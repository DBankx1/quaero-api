BUSINESS_SEARCH_INDEX = {
  "mappings": {
    "dynamic": False,
    "fields": {
      "name": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "category_slugs": {
        "type": "autocomplete"
      },
      "address": {
        "type": "document",
        "fields": {
          "city": { "type": "string" },
          "country": { "type": "string" }
        }
      }
    }
  }
}

CATEGORY_SEARCH_INDEX = {
  "mappings": {
    "dynamic": False,
    "fields": {
      "name": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "slug": {
        "type": "string"
      },
      "primary": {
        "type": "string"
      },
      "secondary": {
        "type": "string"
      },
      "parent_slug": {
        "type": "string"
      }
    }
  }
}

