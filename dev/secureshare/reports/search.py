import re

from django.db.models import Q
from .models import Report
from django.shortcuts import render_to_response


def normalize(query_string, # this method was written based on the method found at http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]



def query(query_string, search_fields):

    query = None
    q_terms = normalize(query_string)

    for term in q_terms:

        or_q = None

        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_q is None:
                or_q = q
            else:
                or_q = or_q | q
        if query is None:
            query = or_q
        else:
            query = query & or_q
    return query


def search( request ):
    query = ''
    found_records = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']

        entry_query = query(query, ['title', 'body', ]) # call the query method

        found_records = Report.objects.filter(entry_query)

        return render_to_response(
                                  'reports/search.html', # results page
                                  {'query_string': query, 'found_entries': found_records} )