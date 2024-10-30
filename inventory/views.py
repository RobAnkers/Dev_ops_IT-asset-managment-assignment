# views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

# View for rendering the index/homepage


class Index(TemplateView):
    template_name = "inventory/index.html"


# View for the user's dashboard, requires login
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch items belonging to the current user and order them by ID
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by("id")

        # Check for low inventory items
        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        )

        # Display a message for low inventory items
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(
                    request, f"{low_inventory.count()} items have a low stock level"
                )
            else:
                messages.error(
                    request, f"{low_inventory.count()} item has a low stock count"
                )

        # Get IDs of low inventory items
        low_inventory_ids = InventoryItem.objects.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        ).values_list("id", flat=True)

        # Render the dashboard template with item data and low inventory IDs
        return render(
            request,
            "inventory/dashboard.html",
            {"items": items, "low_inventory_ids": low_inventory_ids},
        )


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")

# View for user registration/signup


class SignUpView(View):
    def get(self, request):
        # Render the signup form
        form = UserRegisterForm()
        return render(request, "inventory/signup.html", {"form": form})

    def post(self, request):
        # Handle form submission for user registration
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # Save the form data
            form.save()
            # Authenticate and log in the user
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            # Redirect to the index/homepage after successful registration
            return redirect("index")

        # Render the signup form again if form is invalid
        return render(request, "inventory/signup.html", {"form": form})


# View for adding new inventory items, requires login
class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        # Pass category data to the form template
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        # Associate the item with the current user before saving
        form.instance.user = self.request.user
        return super().form_valid(form)


# View for editing existing inventory items, requires login
class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Update was entered correctly.')
        return response


# View for deleting existing inventory items, requires login
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = "inventory/delete_item.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "item"


def simple_logout(request):
    # Log out the user
    logout(request)
    # Redirect the user to the login page
    return HttpResponseRedirect(reverse('login'))


# Function to check if the user is an admin
def is_admin(user):
    return user.is_superuser


@login_required  # Requires user to be logged in
@user_passes_test(is_admin)  # Requires user to pass the is_admin test
def admin_view(request):
    users = User.objects.all()
    user_items = {}
    # Iterate over each user
    for user in users:
        # Filter inventory items by the current user
        items = InventoryItem.objects.filter(user=user).select_related('category')
        # Add the items to the user_items dictionary
        user_items[user] = items
    # Render the admin view template with the user_items dictionary
    return render(request, 'inventory/admin_view.html', {'user_items': user_items})


# View for the about page
def about(request):
    # Render the about template
    return render(request, 'inventory/about.html')
