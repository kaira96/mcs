/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(e){var n;(n=e&&e.fn&&e.fn.select2&&e.fn.select2.amd?e.fn.select2.amd:n).define("select2/i18n/es",[],function(){return{errorLoading:function(){return"No se pudieron cargar los resultados"},inputTooLong:function(e){e=e.input.length-e.maximum;return"Por favor, elimine "+e+" car"+(1==e?"ácter":"acteres")},inputTooShort:function(e){e=e.minimum-e.input.length;return"Por favor, introduzca "+e+" car"+(1==e?"ácter":"acteres")},loadingMore:function(){return"Cargando más resultados…"},maximumSelected:function(e){var n="Sólo puede seleccionar "+e.maximum+" elemento";return 1!=e.maximum&&(n+="s"),n},noResults:function(){return"No se encontraron resultados"},searching:function(){return"Buscando…"},removeAllItems:function(){return"Eliminar todos los elementos"}}}),n.define,n.require},event=new CustomEvent("dal-language-loaded",{lang:"es"});document.dispatchEvent(event);