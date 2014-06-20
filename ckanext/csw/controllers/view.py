import json, re
import xml.etree.ElementTree as etree
try:
    xml_parser_exception = etree.ParseError
except AttributeError:
    from xml.parsers import expat
    xml_parser_exception = expat.ExpatError
import ckan.plugins as p
from ckan import model
from ckan.lib.base import BaseController, c, abort, response
from pylons.i18n import _

class ViewController(BaseController):
    def show_object(self, id):
        try:
            context = {'model': model, 'user': c.user}
            obj = p.toolkit.get_action('iso_metadata')(context, {'id': id})
            response.content_type = 'application/xml; charset=utf-8'
            response.headers['Content-Length'] = len(obj)
            return obj.encode('utf-8')


#           try:
#                if obj['result']:
#                    content = obj['result']
#                else:
#                    abort(404, _('No content found'))
#
#                try:
#
#                except:
#
#            except xml_parser_exception:
#                try:
#                    pkg = json.dumps(content)
#                    response.content_type = 'application/json; charset=utf-8'
#                    response.headers['Content-Length'] = len(obj)
#                    return pkg.encode('utf-8')

        except p.toolkit.ObjectNotFound, e:
            abort(404, _(str(e)))
        except p.toolkit.NotAuthorized:
            abort(401, self.not_auth_message)
        except Exception, e:
            msg = 'An error ocurred: [%s]' % str(e)
            abort(500)