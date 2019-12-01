class SetField  extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
      var element = this.getAttribute('element');
      var title = this.getAttribute('title');
      jQuery(element).html(title);
  }
}

window.customElements.define('set-field', SetField);
