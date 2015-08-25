// adapted from: http://stackoverflow.com/questions/25182303/how-to-wrap-text-in-django-adminset-column-width
/*
 * <-- add to admin.py -->
 * class ClassAdmin(admin.ModelAdmin):
 *     class Media:
 *         js = ('js/save_me_genie.js', # warns before leaving page without saving
 *               'js/jquery.js',
 *               'js/jquery.expander.min.js', # expands/collapses text fields
 *               'js/wordwrap_config.js'),    # implements expand/collapse to table fields
 */
;
$(document).ready(function() {
   $('#result_list tbody tr td').each(function(e) {
        $(this).expander({
            slicePoint:       120,  // default is 100
            expandSpeed: 0,
            expandEffect: 'show',
            collapseSpeed: 0,
            collapseEffect: 'hide',
            expandPrefix:     ' ', // default is '... '
            expandText:       '[...]', // default is 'read more'
            userCollapseText: '[^]'  // default is 'read less'
        });
   });
});
