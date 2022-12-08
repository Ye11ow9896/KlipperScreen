import gi
import logging
import re

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return FWRetractionPanel(*args)


class FWRetractionPanel(ScreenPanel):
    values = {}
    list = {}

    def initialize(self):

        self.grid = Gtk.Grid()

        retract_length = 20
        retract_speed = 50
        unretract_extra_length = 50
        unretract_speed = 10
        tube_length_extr1 = 1165
        tube_length_extr2 = 1165
        

        self.options = [
            {"ret_length": {
                "section": "main", 
                "name": _("Retraction Length"),
                "units": _("mm"),
                "value": retract_length,
                "digits": 0,
                "maxval": 500}},
            {"ret_speed": {
                "section": "main", 
                "name": _("Retraction Speed"),
                "units": _("mm/s"),
                "value": retract_speed,
                "digits": 0,
                "maxval": 100}},
            {"tube_length_extr1": {
                "section": "main", 
                "name": _("Tube length extruder 0"),
                "units": _("mm"),
                "value": tube_length_extr1,
                "digits": 0,
                "maxval": 4000}},
             {"tube_length_extr2": {
                "section": ('main'),
                "name": _("Tube length extruder 1"),
                "units": _("mm"),
                "value": tube_length_extr2,
                "digits": 0,
                "maxval": 4000}},
            {"unret_extra_length": {
                "section": ('main'),
                "name": ("Unretract Extra Length"),
                "units": _("mm"),
                "value": unretract_extra_length,
                "digits": 0,
                "maxval": 150}},
            {"unret_speed": {   
                "name": ("Unretract Speed"),
                "section": ('main'),
                "units": _("mm/s"),
                "value": unretract_speed,
                "digits": 0,
                "maxval": 100}}
        ]

        for option in self.options:
            name = list(option)[0]
            pole = option[name]
            self.add_option(name, pole['name'], pole['units'], pole['value'], pole['digits'], pole["maxval"], pole['section'])

        scroll = self._gtk.ScrolledWindow()
        scroll.add(self.grid)

        self.content.add(scroll)
        self.content.show_all()


    def update_option(self, option, value):
        if option not in self.list:
            return

        if self.list[option]['scale'].has_grab():
            return

        self.values[option] = float(value)
        self.list[option]['scale'].disconnect_by_func(self.set_opt_value)
        self.list[option]['scale'].set_value(self.values[option])
        self.list[option]['scale'].connect("button-release-event", self.set_opt_value, option)

    def add_option(self, option, optname, units, value, digits, maxval, section):
        logging.info("Adding option: %s" % option)

        name = Gtk.Label()
        name.set_markup("<big><b>%s</b></big> (%s)" % (optname, units))
        name.set_hexpand(True)
        name.set_vexpand(True)
        name.set_halign(Gtk.Align.START)
        name.set_valign(Gtk.Align.CENTER)
        name.set_line_wrap(True)
        name.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        
        val = int(self._config.get_config().get(section, option, fallback=value))
        adj = Gtk.Adjustment(val, 0, maxval, 1, 5, 0)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_value(val)
        scale.set_digits(digits)
        scale.set_hexpand(True)
        scale.set_has_origin(True)
        scale.get_style_context().add_class("option_slider")
        scale.connect("button-release-event", self.scale_moved, section, option)

        #reset = self._gtk.ButtonImage("refresh", None, "color1")
        #reset.connect("clicked", self.reset_value, option)
        #reset.set_hexpand(False)

        item = Gtk.Grid()
        item.attach(name, 0, 0, 2, 1)
        item.attach(scale, 0, 1, 1, 1)
        #item.attach(reset, 1, 1, 1, 1)

        frame = Gtk.Frame()
        frame.get_style_context().add_class("frame-item")
        frame.add(item)

        self.list[option] = {
            "row": frame,
            "scale": scale,
        }

        opt = sorted(self.list)
        pos = opt.index(option)
        self.grid.insert_row
        self.grid.attach(self.list[option]['row'], 0, pos, 1, 1)
        self.grid.show_all()

    #def reset_value(self, widget, option):
    #    for x in self.options:
    #        if x["option"] == option:
    #            self.update_option(option, x["value"])
    #    self.set_opt_value(None, None, option)
