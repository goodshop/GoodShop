$('.product-qty').change(function(){
    id = $(this).attr('data-id')
    qty = $(this).val()
    if (qty == '') qty = 1;

    window.location = window.location.origin + window.location.pathname+"update?sku="+id+"&qty="+qty
});

shift_pressed = false;

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
            //alert("key pressed:"+key);
            if (key == 16) {
                shift_pressed = true;
            }
            if (shift_pressed) {
                //alert("Shift is pressed: "+shift_pressed)
                return false;
            }
            return (
                key == 8 ||
                key == 9 ||
                key == 13 ||
                key == 46 ||
                key == 110 ||
                //key == 190 || Disable period
                (key >= 35 && key <= 40) || //Disable %&/()=
                (!shift_pressed && key >= 48 && key <= 57) ||
                (key >= 96 && key <= 105)
                );
        });

        $(this).keyup(function(e)
        {
            var key = e.charCode || e.keyCode || 0;
            if (key == 16) {
                shift_pressed = false;
            }
            return false;
        });
    });
};

$(".product-qty").ForceNumericOnly();