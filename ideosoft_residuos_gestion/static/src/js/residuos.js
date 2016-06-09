$(function() {
   
    "use strict";
   
    var residuo = openerp.residuo = {};
    
    
    residuo.hide_menu_gestion = openerp.Widget.extend({
        hide_menu: function() {
            var model_e = new openerp.Model('residuo.entrada');
            model_e.call('hide_menu_group_gestion')
            .then(function(action) {
                if(action==='hide') {

                    $(".oe_secondary_menu > ul > li:nth-child(2)").css('display', 'none');
                    $(".oe_secondary_menu > div:nth-child(3)").css('display', 'none');
                    $(".oe_secondary_menu > ul:nth-child(4)").css('display', 'none');
                }
            });
        }
    });
    
    
    
    residuo.residuoTopButton = openerp.Widget.extend({
        template:'residuo.btnChangeCompany',
        events: {
            "click": "clicked",
        },
        clicked: function(ev) {
            ev.preventDefault();
            this.trigger("clicked");
        },
    });
    
    
    residuo.companyWidget = openerp.Widget.extend({
        "template": "residuo.company",
        events: {
            "click": "select_company",
        },
        init: function(parent, company) {
            this._super(parent);
            this.set("id", company.id);
            this.set("name", company.name);
            this.set("logo", company.logo);
        },
        start: function(){
        },
        select_company: function() {
            
            var model = new openerp.Model('residuo.entrada');
            model.call('set_user_company',[this.get('id')])
            .then(function(result){
                console.log(result);
                location.reload();
            });
        },
    });
    
    
    residuo.residuoWindowCompaniesWidget = openerp.Widget.extend({
        template:'residuo.selectCompany',
        events: {
            'click .oe_residuo_logo_company': 'toggle_template'
        },
        init: function(parent) {
            this._super(parent);
            this.shown = false;
            this.set("right_offset", 0);
            this.window_h = $(window).height();
            this.window_w = $(window).width();
            this.companies = this.get_companies();
        },
        start: function() {
            this.$el.css('width', this.window_w/2);
            this.$el.css('height', this.window_h/2);
            this.$el.css("right", -this.$el.outerWidth());
            $(window).scroll(_.bind(this.calc_box, this));
            $(window).resize(_.bind(this.calc_box, this));
            this.calc_box();
        },
        get_companies: function() {
            
            var companies = [];
            
            var model_e = new openerp.Model('residuo.entrada');
            model_e.call('get_companies_current_user')
            .then(function(c) {
                companies.push(c);
            });
  
            return companies;
        },
        calc_box: function() {
            var $topbar = window.$('#oe_main_menu_navbar');
            var top = $topbar.offset().top + $topbar.height();
            top = Math.max(top - $(window).scrollTop(), 0);
            this.$el.css("top", top);
            this.$el.css("bottom", 0);
        },
        toggle_template: function() {
            
            var self = this;
            
            var to_erase_widgets = self.widgets;
            self.widgets = {};
            _.each(this.companies[0], function(c) {

                var widget = new openerp.residuo.companyWidget(self, c);
                widget.appendTo(self.$(".oe_residuos_empresas"));
                self.widgets[c.id] = widget;
            });
            _.each(to_erase_widgets, function(to_erase) {
                to_erase.destroy();
            });
            
            this.calc_box();
            var fct =  _.bind(function(place) {
                this.set("right_offset", place + this.$el.outerWidth());
            }, this);
            var opt = {
                step: fct,
            };
            if (this.shown) {
                this.$el.animate({
                    right: -this.$el.outerWidth(),
                }, opt);
            } else {
                this.$el.animate({
                    right: this.window_w/2 - this.$el.outerWidth()/2,
                }, opt);
            }
            this.shown = ! this.shown;
        },
    });
    
    
    if(openerp.web && openerp.web.UserMenu) {
        openerp.web.UserMenu.include({
            do_update: function(){
                var self = this;
                self.update_promise.then(function() {
                    var res = new openerp.residuo.residuoWindowCompaniesWidget(this);
                    var button = new openerp.residuo.residuoTopButton(this);
                    button.appendTo(window.$('.oe_systray'));
                    button.on("clicked", res, res.toggle_template);
                    res.appendTo(window.$('.navbar'));
                    
                    //Ocultar menu de administracion a grupo de gestion
                    var vic = new openerp.residuo.hide_menu_gestion(this);
                    vic.hide_menu();
                });
                return this._super.apply(this, arguments);
            },
        });
    }

    return residuo;
   
    
});