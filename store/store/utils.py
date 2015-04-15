from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def make_page(object_list, page, per_page=8, neighbor_count=5):
    """Return a Django Page object with a list of neighbor pages.

    "neighbor pages" is some pages next to the current page.
    e.g. page 6 may has neighbor page 5, 4, 3 and 7, 8, 9.

    page.neighbor_pages is a list of tuples, which combine the page
    number and a boolean (is it current page)."""
    paginator = Paginator(object_list, per_page)

    # Reference:
    # https://docs.djangoproject.com/en/1.7/topics/pagination/#using-paginator-in-a-view

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    # Neighbor pages will be displayed so that user can select them quickly.
    # Generate a list of neighbor pages enable template can generate them easily.
    start = page.number - neighbor_count // 2
    if start <= 0:
        start = 1
    end = start + neighbor_count
    if end > page.paginator.num_pages + 1:
        end = page.paginator.num_pages + 1

    page.neighbor_pages = [(p, p == page.number) for p in range(start, end)]

    return page
