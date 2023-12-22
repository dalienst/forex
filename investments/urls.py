from django.urls import path

from investments.views import (
    InvestCategoryCreateView,
    InvestCategoryDetailView,
    InvestCategoryListView,
    InvestCategoryUpdateView,
    portfolio,
    PackageCreateView,
    PackageListView,
    PackageDetailView,
    DepositResultsView,
    # PackageWalletDetail,
)

app_name = "investments"

urlpatterns = [
    path("portfolio/", portfolio, name="portfolio"),
    path(
        "category/create/", InvestCategoryCreateView.as_view(), name="investment-create"
    ),
    path(
        "pack/<str:pk>/detail/",
        InvestCategoryDetailView.as_view(),
        name="investment-detail",
    ),
    path(
        "category/update/<str:pk>/",
        InvestCategoryUpdateView.as_view(),
        name="investment-update",
    ),
    path("packs/", InvestCategoryListView.as_view(), name="investment-list"),
    path("package/create/", PackageCreateView.as_view(), name="package-create"),
    path("packages/", PackageListView.as_view(), name="package-list"),
    path(
        "packages/<str:pk>/detail/", PackageDetailView.as_view(), name="package-detail"
    ),
    # path("wallet/<str:pk>/package/", PackageWalletDetail.as_view(), name="package-wallet"),
    path("deposit/", DepositResultsView.as_view(), name="endpoint-deposit"),
]
