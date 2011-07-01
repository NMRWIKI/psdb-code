from coffin import template
from wikimarkup import parse

register = template.Library()

register.filter('mediawikiparse', parse)
