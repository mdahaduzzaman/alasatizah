from django.urls import path

from posts.views import (
    job_post_list_view,
    job_post_detail_view,
    job_post_create_view,
    job_post_update_view,
    my_job_posts_view,
    job_request_list_view,
    job_request_detail_view,
    job_request_create_view,
    job_request_update_view,
    my_job_requests_view,
)


urlpatterns = [
    path("job-posts/add/", job_post_create_view, name="job_post_create"),
    path("job-posts/edit/<uuid:pk>/", job_post_update_view, name="job_post_update"),
    path("job-posts/<uuid:pk>/", job_post_detail_view, name="job_post_detail"),
    path("job-posts/", job_post_list_view, name="job_post_list"),
    path(
        "dashboard/my-jobs/",
        my_job_posts_view,
        name="my_job_posts",
    ),
    path("job-requests/add/", job_request_create_view, name="job_request_create"),
    path("job-requests/edit/<uuid:pk>/", job_request_update_view, name="job_request_update"),
    path("job-requests/<uuid:pk>/", job_request_detail_view, name="job_request_detail"),
    path("job-requests/", job_request_list_view, name="job_request_list"),
    path(
        "dashboard/my-requests/",
        my_job_requests_view,
        name="my_job_requests",
    ),
]
