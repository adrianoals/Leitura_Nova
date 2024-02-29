document.addEventListener('DOMContentLoaded', function() {
    var viewportMeta = document.querySelector('meta[name="viewport"]');
    document.querySelectorAll('input, select, textarea').forEach(function(el) {
        el.addEventListener('focus', function() {
            viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0');
        });
        el.addEventListener('blur', function() {
            viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1.0');
        });
    });
});
