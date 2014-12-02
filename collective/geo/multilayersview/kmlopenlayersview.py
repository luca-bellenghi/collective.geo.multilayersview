from zope.interface import implements

from Products.Five import BrowserView

from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from plone.memoize.instance import memoizedproperty
from zope.interface import Interface


class IMultiLayersView(Interface):
    """ """


class KMLFile(BrowserView):

    """ Kml Openlayers View """
    def get_data(self):
        return self.context.getFile().data


class KmlOpenLayersView(BrowserView):
    """ Kml Openlayers View """

    implements(IMultiLayersView)


class KMLMapLayer(MapLayer):
    """map layer see: collective.geo.mapwidget
    """
    @memoizedproperty
    def jsfactory(self):
        title = self.context.Title().replace("'", "\'")
        template = self.context.restrictedTraverse('kml-searchlayers')()
        return template % (title, self.context.absolute_url())


class KMLMapLayers(MapLayers):
    '''create all layers for this view.
    '''
    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        for item in self.context.getFolderContents():
            layers.append(KMLMapLayer(context=item.getObject()))
        return layers
