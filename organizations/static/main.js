var makeKeyHandler = function(key, callback){
    return function(e){
        if ((e.which && e.which == key) || (e.keyCode && e.keyCode == key)){
            callback(e);
            e.stopImmediatePropagation();
        }
    };
};


var setupButtonEventHandlers = function(button, callback){
    var wrapped_callback = function(e){
        callback();
        e.stopImmediatePropagation();
    };
    button.keydown(makeKeyHandler(13, wrapped_callback));
    button.click(wrapped_callback);
};

/* some google closure-like code for the ui elements */
var inherits = function(childCtor, parentCtor) {
  /** @constructor taken from google closure */
    function tempCtor() {};
    tempCtor.prototype = parentCtor.prototype;
    childCtor.superClass_ = parentCtor.prototype;
    childCtor.prototype = new tempCtor();
    childCtor.prototype.constructor = childCtor;
};

/* wrapper around jQuery object */
var WrappedElement = function(){
    this._element = null;
    /**
     * @private
     * @type {boolean}
     */
    this._in_document = false;
    /**
     * @private
     * @type {Array.<string>}
     */
    this._css_classes = [];
    /**
     * @private
     * @type {string}
     */
    this._html_tag = 'div';
};
WrappedElement.prototype.setElement = function(element){
    this._element = element;
};
WrappedElement.prototype.setHtmlTag = function(html_tag){
    this._html_tag = html_tag;
};
/**
 * @param {string} css_class
 */
WrappedElement.prototype.addClass = function(css_class){
    if ($.inArray(css_class, this._css_classes) > -1){
        return;
    } else {
        this._css_classes.push(css_class);
        if (this._element){
            this._element.addClass(css_class);
        }
    }
};
/**
 * @param {css_class}
 */
WrappedElement.prototype.removeClass = function(css_class){
    if ($.inArray(css_class, this._css_classes) > 1){
        arrayRemove(this._css_classes, css_class);
        if (this._element){
            this._element.removeClass(css_class);
        }
    }
};
WrappedElement.prototype.setCssClasses = function(){
    if (this._css_classes){
        var element = this.getElement();
        $.each(this._css_classes, function(idx, css_class){
            element.addClass(css_class);
        });
    }
};
WrappedElement.prototype.createDom = function(){
    this._element = this.makeElement(this._html_tag);
    if (this._css_classes.length > 0){
        var element = this._element;
        $.each(this._css_classes, function(idx, css_class){
            element.addClass(css_class);
        });
    }
};
WrappedElement.prototype.getElement = function(){
    if (this._element === null){
        this.createDom();
    }
    return this._element;
};
/**
 * @param {Array.<string>} events
 * event names must be real - no error checking
 */
WrappedElement.prototype.stopEventPropagation = function(events){
    var elem = this.getElement();
    $.each(events, function(idx, event_name){
        elem[event_name](function(e){
            e.stopImmediatePropagation();
        });
    });
};
WrappedElement.prototype.inDocument = function(){
    return this._in_document;
};
WrappedElement.prototype.enterDocument = function(){
    return this._in_document = true;
};
WrappedElement.prototype.hasElement = function(){
    return (this._element !== null);
};
WrappedElement.prototype.makeElement = function(html_tag){
    //makes jQuery element with tags
    return $('<' + html_tag + '></' + html_tag + '>');
};
WrappedElement.prototype.dispose = function(){
    if (this._element){
        this._element.remove();
    }
    this._in_document = false;
};

var SimpleControl = function(){
    WrappedElement.call(this);
    this._handler = null;
    this._title = null;
};
inherits(SimpleControl, WrappedElement);

SimpleControl.prototype.setHandler = function(handler){
    this._handler = handler;
    if (this.hasElement()){
        this.setHandlerInternal();
    }
};

SimpleControl.prototype.setHandlerInternal = function(){
    //default internal setHandler behavior
    setupButtonEventHandlers(this._element, this._handler);
};

SimpleControl.prototype.setTitle = function(title){
    this._title = title;
};

/**
 * A clickable icon
 * @constructor
 * @param {string} icon_class - class name for the icon
 * @param {string} title - to become "title" attribute
 */
var ActionIcon = function(icon_class, title){
    SimpleControl.call(this);
    this._class = icon_class;
    this._title = title
};
inherits(ActionIcon, SimpleControl);
/**
 * @private
 */
ActionIcon.prototype.createDom = function(){
    this._element = this.makeElement('span');
    this.decorate(this._element);
};
/**
 * @param {Object} element
 */
ActionIcon.prototype.decorate = function(element){
    this._element = element;
    this._element.addClass(this._class);
    this._element.attr('title', this._title);
    if (this._handler !== null){
        this.setHandlerInternal();
    }
};

var EditLink = function(){
    SimpleControl.call(this)
};
inherits(EditLink, SimpleControl);

EditLink.prototype.createDom = function(){
    var element = $('<a></a>');
    element.addClass('edit');
    this.decorate(element);
};

EditLink.prototype.decorate = function(element){
    this._element = element;
    this._element.html('edit');
    this.setHandlerInternal();
};

/**
 * @constructor
 * @param {string} title
 */
var DeleteIcon = function(title){
    ActionIcon.call(this, 'delete-icon', title);
};
inherits(DeleteIcon, ActionIcon);

var AdderIcon = function(title){
    ActionIcon.call(this, 'adder-icon', title);
};
inherits(AdderIcon, ActionIcon);

/**
 * @constructor
 * a wrapped jquery element that has state
 */
var Widget = function(){
    WrappedElement.call(this);
    /**
     * @private
     * @type {Object.<string, Function>}
     * "dictionary" of transition state event handlers
     * where keys are names of the states to which 
     * the widget is transitioning
     * and the values are functions are to be called upon
     * the transitions
     */
    this._state_transition_event_handlers = {};
    /** 
     * @private
     * @type {string}
     * internal state of the widget
     */
    this._state = null;
};
inherits(Widget, WrappedElement);

Widget.prototype.getStateTransitionEventHandlers = function(){
    return this._state_transition_event_handlers;
};

/**
 * @param {Widget} other_widget
 * not a careful method, will overwrite all
 */
Widget.prototype.copyStateTransitionEventHandlersFrom = function(other_widget){
    this._state_transition_event_handlers =
        other_widget.getStateTransitionEventHandlers();
};
/**
 * @private
 */
Widget.prototype.backupStateTransitionEventHandlers = function(){
    this._steh_backup = this._state_transition_event_handlers;
};
/**
 * @private
 */
Widget.prototype.restoreStateTransitionEventHandlers = function(){
    this._state_transition_event_handlers = this._steh_backup;
};
/**
 * @param {string} state
 */
Widget.prototype.setState = function(state){
    this._state = state;
};
/**
 * @return {sting} state
 */
Widget.prototype.getState = function(){
    return this._state;
};

/**
 * @param {Object}
 */
Widget.prototype.setStateTransitionEventHandlers = function(handlers){
    this._state_transition_event_handlers = handlers;
};

//custom autocompleter

/**
 * A text element with an "edit" prompt
 * showing on mouseover
 * the widget has two states: DISPLAY and "EDIT"
 * when user hits "edit", widget state changes to
 * EDIT, when user hits "enter" state goes to "DISPLAY
 * replaced with an input box and the "edit" link
 * hides
 * when user hits "enter", 
 */
var EditableString = function(){
    Widget.call(this);
    /**
     * @private
     * @type {string}
     * text string that is to be shown 
     * to the user
     */
    this._text = '';

    /**
     * @private
     * @type {boolean}
     */
    this._is_editable = true;
    /**
     * @private
     * @type {string}
     * supported states are 'DISPLAY' and 'EDIT'
     * 'DISPLAY' is default
     */
    this._state = 'DISPLAY';
    /**
     * @private
     * @type {boolean}
     */
    this._is_multiline = false;
};
inherits(EditableString, Widget);

/**
 * @param {boolean} is_editable
 */
EditableString.prototype.setEditable = function(is_editable){
    this._is_editable = is_editable;
};

/**
 * @param {boolean}
 */
EditableString.prototype.isEditable = function(){
    return this._is_editable;
};

/**
 * @param {boolean} is_multiline
 */
EditableString.prototype.setMultiline = function(is_multiline){
    this._is_multiline = is_multiline;
};

/**
 * @return {Object}
 */
EditableString.prototype.getDisplayBlock = function(){
    return this._display_block;
};
/**
 * @return {Object}
 */
EditableString.prototype.getEditBlock = function(){
    return this._edit_block;
};

EditableString.prototype.setState = function(state){
    if (state === 'EDIT' && this.isEditable() === false){
        throw 'cannot edit this instance of EditableString';
    }

    this._state = state;

    //run transition event handler, if exists
    var handlers = this.getStateTransitionEventHandlers();
    if (handlers.hasOwnProperty(state)){
        handlers[state].call();
    }

    if (! (this._display_block && this._edit_block) ){
        //a case when createDom has not yet been called
        return;
    }

    //hide and show things
    if (state === 'EDIT'){
        this._edit_block.show();
        this._input_box.focus();
        this._display_block.hide();
    } else if (state === 'DISPLAY'){
        this._edit_block.hide();
        this._display_block.show();
        if (this.isEditable()){
            this._edit_link.show();
        }
    }
};

/**
 * @param {string} text - string text
 */
EditableString.prototype.setText = function(text){
    this._text = text;
    if (this._text_element){
        this._text_element.html(text);
    };
};

/**
 * @return {string} text of the string
 */
EditableString.prototype.getText = function(){
    if (this._text_element){
        var text = $.trim(this._text_element.html());
        this._text = text;
        return text;
    } else {
        return $.trim(this._text);
    }
};

/**
 * @return {string}
 */
EditableString.prototype.getInputBoxText = function(){
    return $.trim(this._input_box.val());
};

EditableString.prototype.getSaveEditHandler = function(){
    var me = this;
    return function(){
        me.setText(me.getInputBoxText());
        me.setState('DISPLAY');
    };
};

EditableString.prototype.getStartEditHandler = function(){
    var me = this;
    return function(){
        me.setState('EDIT');
        me._input_box.val(me._text_element.html());
        me._input_box.focus();
    };
};

/** override me */
EditableString.prototype.getTextClickHandler = function(){
    return function(){};
};

/**
 * takes an jQuery element, assumes (no error checking)
 * that the element
 * has a single text node and replaces its content with
 * <div><span>text</span><a>edit</a><div>
 * <div><input /></div>
 * and enters the DISPLAY state
 */
EditableString.prototype.decorate = function(element){
    this.setText(element.html());//no error checking
    //build dom for the display block
    var real_element = this.getElement();
    this._element = element;
    this._element.empty();
    this._element.append(real_element);
};

EditableString.prototype.createDom = function(){

    this._element = this.makeElement('div');

    this._display_block = this.makeElement('div');
    this._element.append(this._display_block);
    this._text_element = this.makeElement('div');
    this._display_block.append(this._text_element);
    //set the value of text
    this._text_element.html(this._text);
    //set the display state

    //it is assumed that _is_editable is set once at the beginning
    this._edit_block = this.makeElement('div');
    this._element.append(this._edit_block);

    if (this._is_multiline === false){
        this._edit_block.css('display', 'inline');
        this._display_block.css('display', 'inline');
        this._input_box = this.makeElement('input');
        this._input_box.attr('type', 'text');
    } else {
        this._input_box = this.makeElement('textarea');
    }
    this._edit_block.append(this._input_box);


    var edit_link = new EditLink();
    edit_link.setHandler(
        this.getStartEditHandler()
    );

    var edit_element = edit_link.getElement();
    if (!this.isEditable()){
        edit_element.hide();
    }
    this._display_block.append(edit_element);
    //build dom for the edit block

    this._edit_link = edit_link.getElement();

    this._text_element.click(this.getTextClickHandler());

    if (this._is_multiline === false){
        this._input_box.keydown(
            makeKeyHandler(13, this.getSaveEditHandler())
        );
    }
    this.setState(this.getState());
};

var Description = function(){
    EditableString.call(this);
    /**
     * @type {boolean}
     */
    this._is_multiline = false;
    /**
     * @type {?number}
     */
    this._id = null;
    /**
     * @type {string}
     */
    this._field = null;
    /**
     * @type {string}
     */
    this._model = null;
}
inherits(Description, EditableString);

Description.prototype.getObjectId = function(){
    return this._id;
};

Description.prototype.getObjectField = function(){
    return this._field;
};

Description.prototype.setObjectId = function(id){
    this._id = id;
};

Description.prototype.setObjectField = function(model, field){
    this._model = model;
    this._field = field;
};

Description.prototype.saveTextToDb = function(on_save){
    var me = this;
    var id = me._id;
    var field = me._field;
    $.ajax({
        type: 'POST',
        url: orgs['urls']['save_org_description'],
        data: {text: me.getInputBoxText(), id: id, field: field},
        dataType: 'json',
        cache: false,
        success: on_save
    });
};

Description.prototype.getSaveEditHandler = function(){
    var me = this;
    return function(){
        var on_finish = function(data){
            me.setText(data['text']);
            me.setState('DISPLAY');
        };
        me.saveTextToDb(on_finish);
    }; 
};

Description.prototype.getCancelEditHandler = function(){
    var me = this;
    return function(){
        me.setState('DISPLAY');
    };
};

Description.prototype.getStartEditHandler = function(){
    var me = this;
    var field = this._field;
    var on_load = function(data){
        me.setState('EDIT');
        me._input_box.val(data['text']);
        me._input_box.focus();
    };
    return function(){
        $.ajax({
            url: orgs['urls']['get_org_description'],
            data: {id: me.getObjectId(), field: field},
            dataType: 'json',
            type: 'GET',
            success: on_load
        });
    }
};


Description.prototype.decorate = function(element){
    Description.superClass_.decorate.call(this, element);
    var edit_block = this.getEditBlock();
    var button = this.makeElement('button');
    button.html("Save");
    setupButtonEventHandlers(button, this.getSaveEditHandler());
    edit_block.append(button);
    var button2 = this.makeElement('button');
    button2.html("Cancel");
    setupButtonEventHandlers(button2, this.getCancelEditHandler());
    edit_block.append(button2);
};

