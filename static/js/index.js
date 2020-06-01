

/*  --------    Recipe New    --------  */

// --    Button for adding rows   --
jQuery(function($) {
    var $button = $('#add-row'),
        $row = $('.directions').clone();

    $button.click(function() {
        $row.clone().insertBefore( $button );
    });
});​