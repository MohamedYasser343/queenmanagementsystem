from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.db.models import Sum, F

from tapp.forms import CVsForm, CopyingForm, CustomerForm, SelledItemsForm, StorageForm, WritingForm, EntryForm
from .models import CVs, Copying, Customers, Entry, SelledItems, Storage, Writing

@login_required
def index(request):
    return render(request, 'tapp/index.html', {'arabic_name': request.user.arabic_name})

@login_required
def view_entries(request):
    today = timezone.now().date()
    entries = Entry.objects.filter(
        name=request.user,
        timestamp__date=today
    ).order_by('-timestamp')
    
    total_points = Entry.objects.filter(
        name=request.user,
        timestamp__date=today
    ).aggregate(total_points=Sum('points'))['total_points'] or 0

    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tapp/view_entries.html', {
        'page_obj': page_obj,
        'total_points': total_points
    })

@login_required
def add_entry(request):
    form_class = EntryForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.name = request.user
            entry.save()

            user = request.user
            user.points = F('points') + entry.points
            user.save()

            storage = request.user.storage
            storage.quantity = F('quantity') - entry.numeber
            storage.save()

            # add one point to customer
            if entry.customer:
                customer = entry.customer
                customer.points = F('points') + 1
                customer.save()

            return redirect('view_entries')
    else:
        form = form_class()

    return render(request, f'tapp/add_entry.html', {'form': form})

@login_required
def delete_entry(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, id=entry_id)
        entry.delete()
        return redirect('view_entries')
    return HttpResponseForbidden("Method not allowed")

class CustomLoginView(LoginView):
    template_name = 'tapp/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_only')
        return reverse_lazy('index')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect(self.next_page)

@login_required
def admin_only_view(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to view this page.")

    entries = Entry.objects.all().order_by('-timestamp')
    total_price = entries.aggregate(Sum('price'))['price__sum'] or 0

    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tapp/admin_only.html', {
        'page_obj': page_obj,
        'total_price': total_price,
    })

@login_required
def all_deliveries(request):
    cvs = CVs.objects.exclude(status='اتسلم')
    writings = Writing.objects.exclude(status='اتسلم')
    copyings = Copying.objects.exclude(status='اتسلم')
    return render(request, 'tapp/all_deliveries.html', {
        'cvs': cvs,
        'writings': writings,
        'copyings': copyings,
    })

@login_required
def add_deliverable(request, form_class, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.name = request.user
            deliverable.save()
            return redirect('all_deliveries')
    else:
        form = form_class()

    return render(request, template_name, {'form': form})

@login_required
def edit_deliverable(request, model_class, form_class, template_name, deliverable_id):
    deliverable = get_object_or_404(model_class, id=deliverable_id)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=deliverable)
        if form.is_valid():
            # Check if the service is not 'copying' and the status is 'done'
            if form.cleaned_data.get('service') != 'تصوير' and form.cleaned_data.get('status') == 'اتعمل':
                # Check if 'file' field exists in the form
                if 'file' in form.fields and not form.cleaned_data.get('file'):
                    form.add_error('file', 'File upload is required when status is "done".')
                else:
                    form.save()
                    return redirect('all_deliveries')
            else:
                form.save()
                return redirect('all_deliveries')
    else:
        form = form_class(instance=deliverable)

    return render(request, template_name, {'form': form, 'deliverable': deliverable})


@login_required
def delete_deliverable(request, model_class, deliverable_id):
    if request.method == 'POST':
        deliverable = get_object_or_404(model_class, id=deliverable_id)
        deliverable.delete()
        return redirect('all_deliveries')
    return HttpResponseForbidden("Method not allowed")

@login_required
def download_deliverable(request, deliverable_type, delivery_id):
    model_class = {'cvs': CVs, 'writings': Writing, 'copyings': Copying}.get(deliverable_type)
    if model_class is None:
        raise Http404("Invalid deliverable type")
    try:
        deliverable = model_class.objects.get(id=delivery_id)
        file_path = deliverable.file.path
        file_name = deliverable.file.name.split('/')[-1]

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response

    except model_class.DoesNotExist:
        raise Http404("Delivery does not exist")
    except Exception as e:
        raise Http404(f"Error downloading file: {e}")

# Use these functions for add/edit/delete of CVs, Writing, Copying
add_cv = lambda request: add_deliverable(request, CVsForm, 'tapp/add_cv.html')
edit_cv = lambda request, cv_id: edit_deliverable(request, CVs, CVsForm, 'tapp/add_cv.html', cv_id)
delete_cv = lambda request, cv_id: delete_deliverable(request, CVs, cv_id)

add_writing = lambda request: add_deliverable(request, WritingForm, 'tapp/add_writing.html')
edit_writing = lambda request, writing_id: edit_deliverable(request, Writing, WritingForm, 'tapp/add_writing.html', writing_id)
delete_writing = lambda request, writing_id: delete_deliverable(request, Writing, writing_id)

add_copying = lambda request: add_deliverable(request, CopyingForm, 'tapp/add_copying.html')
edit_copying = lambda request, copying_id: edit_deliverable(request, Copying, CopyingForm, 'tapp/add_copying.html', copying_id)
delete_copying = lambda request, copying_id: delete_deliverable(request, Copying, copying_id)

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_customers')
    else:
        form  = CustomerForm()
    return render(request, 'tapp/add_customer.html', {'form': form})

@login_required
def view_customers(request):
    customers = Customers.objects.all().order_by('-id')
    paginator = Paginator(customers, 10)  # Paginate with 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tapp/view_customers.html', {
        'page_obj': page_obj,
    })

@login_required
def delete_customer(request, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customers, id=customer_id)
        customer.delete()
        return redirect('view_customers')
    return HttpResponseForbidden("Method not allowed")

@login_required
def view_storage(request):
    storage = Storage.objects.all().order_by('-id')
    paginator = Paginator(storage, 10)  # Paginate with 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tapp/view_storage.html', {
        'page_obj': page_obj,
    })

@login_required
def add_storage(request):
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_storage')
    else:
        form  = StorageForm()
    return render(request, 'tapp/add_storage.html', {'form': form})

@login_required
def delete_storage(request, storage_id):
    if request.method == 'POST':
        storage = get_object_or_404(Storage, id=storage_id)
        storage.delete()
        return redirect('view_storage')
    return HttpResponseForbidden("Method not allowed")


# view selled items from storage
@login_required
def view_selled_items(request):
    selled_items = SelledItems.objects.all().order_by('-id')
    paginator = Paginator(selled_items, 10)  # Paginate with 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tapp/view_selled_items.html', {
        'page_obj': page_obj,
    })

@login_required
def add_selled_item(request):
    if request.method == 'POST':
        form = SelledItemsForm(request.POST)
        if form.is_valid():
            selled_item = form.save(commit=False)  # Do not save to the database yet
            storage_item = get_object_or_404(Storage, id=selled_item.item.id)
            selled_item.price = storage_item.price * selled_item.quantity
            storage_item.quantity = F('quantity') - selled_item.quantity

            storage_item.save()
            selled_item.save()
            return redirect('view_selled_items')
    else:
        form = SelledItemsForm()
    return render(request, 'tapp/add_selled_item.html', {'form': form})