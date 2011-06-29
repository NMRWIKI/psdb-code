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
