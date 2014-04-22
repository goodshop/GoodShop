$('.product-qty').change(function(){
    id = $(this).attr('data-id')
    qty = $(this).val()
    window.location = window.location.origin + window.location.pathname+"update?sku="+id+"&qty="+qty
});

// Numeric only control handler
jQuery.fn.ForceNumericOnly =
function()
{
    return this.each(function()
    {
        $(this).keydown(function(e)
        {
            var key = e.charCode || e.keyCode || 0;
            // allow backspace, tab, delete, enter, arrows, numbers and keypad numbers ONLY
            // home, end, period, and numpad decimal
            //alert(key);
            return (
                key == 8 ||
                key == 9 ||
                key == 13 ||
                key == 46 ||
                key == 110 ||
                //key == 190 || Disable period
                (key >= 35 && key <= 40) ||
                (key >= 48 && key <= 57) ||
                (key >= 96 && key <= 105));
        });
    });
};

$(".product-qty").ForceNumericOnly();