function fmt_bit(bits) {
    var i = -1;
    var bitUnits = ['kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb'];
    do {
        bits = bits / 1024;
        i++;
    } while (bits > 1024);
    return bits.toFixed(2) + bitUnits[i];
}

function fmt_byte(bytes) {
    var i = -1;
    var byteUnits = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        bytes = bytes / 1024;
        i++;
    } while (bytes > 1024);
    return bytes.toFixed(2) + byteUnits[i];
}

function fmt_time(seconds){
    var date = new Date(1970,0,1);
    date.setSeconds(seconds);
    return date.toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");
}

openerp.web_widget_test = function(instance) {


	
	// Bit
	instance.web.list.Bit = instance.web.list.Column.extend({
		format: function (row_data, options) {
			value = fmt_byte(row_data[this.id].value || 0);
			return instance.web.qweb.render('ListView.row.bit', {widget: this, value: value});
		}
	})
	
	// Byte
	instance.web.list.Byte = instance.web.list.Column.extend({
		format: function (row_data, options) {
			value = fmt_byte(row_data[this.id].value || 0);
			return instance.web.qweb.render('ListView.row.byte', {widget: this, value: value});
		}
	})
	
	// Time
	instance.web.list.Time = instance.web.list.Column.extend({
		format: function (row_data, options) {
			value = fmt_time(row_data[this.id].value || 0);
			return instance.web.qweb.render('ListView.row.time', {widget: this, value: value});
		}
	})
	

	
	
    instance.web.form.FieldBit = instance.web.form.FieldChar.extend({
        widget_class: 'oe_form_field_bit',
        render_value: function () {
            var value = this.format_value(this.get('value'), '');
            if (!this.get("effective_readonly")) {
                var $input = this.$el.find('input');
                $input.val(value);
            } else {
				this.$(".oe_form_char_content").text(fmt_bit(value));
			}
        }
    });
	
    instance.web.form.FieldBit = instance.web.form.FieldChar.extend({
        widget_class: 'oe_form_field_bit',
        render_value: function () {
            var value = this.format_value(this.get('value'), '');
            if (!this.get("effective_readonly")) {
                var $input = this.$el.find('input');
                $input.val(value);
            } else {
				this.$(".oe_form_char_content").text(fmt_byte(value));
			}
        }
    });
	
    instance.web.form.FieldTimeFormat = instance.web.form.FieldChar.extend({
        widget_class: 'oe_form_field_bit',
        render_value: function () {
            var value = this.format_value(this.get('value'), '');
            if (!this.get("effective_readonly")) {
                var $input = this.$el.find('input');
                $input.val(value);
            } else {
				this.$(".oe_form_char_content").text(fmt_time(value));
			}
        }
    });

	instance.web.form.FieldCode = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
		template: 'FieldCode',
		init: function() {
			this._super.apply(this, arguments);
		},
		initialize_content: function() {
			var self = this;
						
			//if (! this.get("effective_readonly")) {
				self._updating_editor = false;
				this.$textarea = this.$el.find('textarea');
				this.$textarea.val(this.get('value') || '');
				self._updating_editor = true;
				
				this.$textarea.css({
					'font-family': 'monospace',
					'white-space': 'pre',
					'background-color': '#FFFFE0',
					'width': '100%',					
				});
				
				if(this.get("effective_readonly")) {
			    	this.$textarea.attr('disabled', 'disabled');
					this.$textarea.attr('readonly', true);
				}
				
				this.$editor = this.$textarea.ace({ lang: this.node.attrs.lang })
			//}
		},
		render_value: function() {
			if (! this.get("effective_readonly")) {
				

				
				if (! this.auto_sized) {
					this.auto_sized = true;
					this.$textarea.autosize();
				} else {
					this.$textarea.trigger("autosize");
				}
				
			} else {
				this.$textarea.val(this.get('value') || '');
			}
				
		},
		commit_value: function () {
			if (! this.get("effective_readonly") && this.$textarea) {
				this.store_dom_value();
			}
			return this._super();
		},
		store_dom_value: function () {
			this.internal_set_value(instance.web.parse_value(this.$textarea.val(), this));
		},
	});
	
    instance.web.form.FieldCode2 = instance.web.form.FieldText.extend({
        widget_class: 'oe_form_field_code',
		render_value: function() {
			if (!this.get("effective_readonly")) {
				var show_value = instance.web.format_value(this.get('value'), this, '');
				if (show_value === '') {
					this.$textarea.css('height', parseInt(this.default_height, 10)+"px");
				}
				this.$textarea.val(show_value);
				
				if (! this.auto_sized) {
					this.auto_sized = true;
					this.$textarea.autosize();
				} else {
					this.$textarea.trigger("autosize");
				}
				
				this.$textarea.css({
					'font-family': 'monospace',
					'white-space': 'pre',
					'background-color': '#FFFFE0',
				});
				this.$editor = this.$textarea.ace({ lang: 'python' })
				
			} else {
				var txt = this.get("value") || '';
				
				this.$(".oe_form_text_content").text(txt).css({
				 	'font-family': 'monospace',
				 	'white-space': 'pre',
				 	'background-color': '#FFFFE0',
				 	'padding': '2px 4px',
				})
				
			}
		}
    });
	
	
	instance.web.list.columns.add('field.bit', 'instance.web.list.Bit');
	instance.web.list.columns.add('field.byte', 'instance.web.list.Byte');
	instance.web.list.columns.add('field.time', 'instance.web.list.Time');

	instance.web.form.widgets.add('bit', 'instance.web.form.FieldBit');
	instance.web.form.widgets.add('byte', 'instance.web.form.FieldByte');
	instance.web.form.widgets.add('time_format', 'instance.web.form.FieldTimeFormat');
	instance.web.form.widgets.add('code', 'instance.web.form.FieldCode');

	

	
	
	
};
