from krita import DockWidgetFactory, DockWidgetFactoryBase
from .OneTimeColorSamplerTool import OneTimeColorSamplerTool

DOCKER_ID = 'OneTimeColorSamplerTool'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        OneTimeColorSamplerTool)

instance.addDockWidgetFactory(dock_widget_factory)
