from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from alasatizah.decorators.profile_required import guardian_or_organization_required, ustaz_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


from guardian.models import Guardian
from organization.models import Organization
from posts.choices import JobStatusChoices
from posts.models import JobPost, UstazJobRequest
from posts.forms import JobPostForm, UstazJobRequestForm
from core.forms import AddressForm


def job_post_list_view(request):
    query = request.GET.get("search", "")
    job_posts = (
        JobPost.objects.select_related("address")
        .filter(is_verified=True, status=JobStatusChoices.PUBLISHED)
        .order_by("-created_at")
    )

    job_posts.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(address__city__icontains=query)
        | Q(address__area__icontains=query)
    )

    paginator = Paginator(job_posts, 10)
    page_number = request.GET.get("page", None)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "posts/job_post_list.html", {"page_obj": page_obj, "query": query})


def job_post_detail_view(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk)
    return render(request, "posts/job_post_detail.html", {"job_post": job_post})


@guardian_or_organization_required
@login_required
def job_post_create_view(request):
    form = JobPostForm(request.POST or None, request.FILES or None)
    address_form = AddressForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()

        guardian = Guardian.objects.filter(user=request.user).first()
        organization = Organization.objects.filter(user=request.user).first()

        job_post: JobPost = form.save(commit=False)
        job_post.address = address
        job_post.content_object = guardian if guardian else organization
        job_post.save()
        return redirect("job_post_list")

    return render(
        request,
        "posts/job_post_create.html",
        {"form": form, "address_form": address_form},
    )


@guardian_or_organization_required
@login_required
def job_post_update_view(request, pk):
    guardian = Guardian.objects.filter(user=request.user).first()
    organization = Organization.objects.filter(user=request.user).first()
    if guardian:
        job_post = get_object_or_404(guardian.job_posts, pk=pk)
    else:
        job_post = get_object_or_404(organization.job_posts, pk=pk)

    form = JobPostForm(request.POST or None, request.FILES or None, instance=job_post)
    address_form = AddressForm(
        request.POST or None, request.FILES or None, instance=job_post.address
    )

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()

        guardian = Guardian.objects.filter(user=request.user).first()
        organization = Organization.objects.filter(user=request.user).first()

        job_post: JobPost = form.save(commit=False)
        job_post.address = address
        job_post.save()
        return redirect("job_post_detail", pk)

    return render(
        request,
        "posts/job_post_create.html",
        {"form": form, "address_form": address_form, "job_post": job_post},
    )


@guardian_or_organization_required
@login_required
def my_job_posts_view(request):
    query = request.GET.get("search", "")
    guardian = Guardian.objects.filter(user=request.user).first()

    organization = Organization.objects.filter(user=request.user).first()

    if guardian:
        # If the user is a guardian, get their job posts
        job_posts = guardian.job_posts.all().order_by("-created_at")
    else:
        # If the user is an organization, get their job posts
        job_posts = organization.job_posts.all().order_by("-created_at")

    job_posts.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(address__city__icontains=query)
        | Q(address__area__icontains=query)
    )

    paginator = Paginator(job_posts, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # passing the owner so that the template can check if the user is the owner of the job posts
    return render(
        request, "posts/job_post_list.html", {"page_obj": page_obj, "owner": True, "query": query}
    )


# Job Requests views
def job_request_list_view(request):
    job_requests = UstazJobRequest.objects.filter(
        is_verified=True, status=JobStatusChoices.PUBLISHED
    ).order_by("-created_at")

    paginator = Paginator(job_requests, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "posts/job_request_list.html", {"page_obj": page_obj})


def job_request_detail_view(request, pk):
    job_request = get_object_or_404(UstazJobRequest, pk=pk)
    return render(request, "posts/job_request_detail.html", {"job_post": job_request})


@ustaz_required
@login_required
def job_request_create_view(request):
    ustaz = request.user.ustaz
    form = UstazJobRequestForm(request.POST or None)
    address_form = AddressForm(request.POST or None)

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()
        job_request: UstazJobRequest = form.save(commit=False)
        job_request.address = address
        job_request.ustaz = ustaz
        job_request.save()
        return redirect("job_request_list")

    return render(request, "posts/job_request_create.html", {"form": form, "address_form": address_form})


@ustaz_required
@login_required
def job_request_update_view(request, pk):
    ustaz = request.user.ustaz
    job_request = get_object_or_404(ustaz.job_requests, pk=pk)
    form = UstazJobRequestForm(request.POST or None, instance=job_request)
    address_form = AddressForm(request.POST or None, instance=job_request.address)

    if request.method == "POST" and form.is_valid() and address_form.is_valid():
        address = address_form.save()
        job_request: UstazJobRequest = form.save(commit=False)
        job_request.address = address
        job_request.save()
        return redirect("job_request_detail", pk)

    return render(request, "posts/job_request_create.html", {"form": form, "instance": job_request, "address_form": address_form})


@ustaz_required
@login_required
def my_job_requests_view(request):
    ustaz = request.user.ustaz
    job_requests = ustaz.job_requests.all().order_by("-created_at")

    paginator = Paginator(job_requests, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "posts/job_request_list.html", {"page_obj": page_obj, "owner": True})
