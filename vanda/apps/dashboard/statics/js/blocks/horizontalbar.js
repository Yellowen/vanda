function HorizontalBar (name, element_selector) {
    Block.call(this, name, element_selector);
};

HorizontalBar.prototype = new Block();
HorizontalBar.prototype.constructor = HorizontalBar;

document.blocks["HorizontalBar"] = HorizontalBar;

