find releases -type f -name "*.yaml" -exec python -m yay releases/insert_release.yay folder="Cool Store" file={} \;
python -m yay dashboards/add_dashboards.yay folder="Cool Store" file=dashboards/cool_store_dashboard.yaml
python -m yay dashboards/add_dashboards.yay folder="Cool Store/Address book" file=dashboards/address_book_dashboard.yaml
python -m yay dashboards/add_dashboards.yay folder="Cool Store/Shopping cart" file=dashboards/shopping_cart_dashboard.yaml
python -m yay dashboards/add_dashboards.yay folder="Cool Store/Wish list" file=dashboards/wish_list_dashboard.yaml
