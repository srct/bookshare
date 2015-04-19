// fancy autopopulation widget
$.widget( "custom.catcomplete", $.ui.autocomplete, {
  _create: function() {
    this._super();
    this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
  },
  _renderMenu: function( ul, items ) {
    var that = this,
      currentDepartment = "";
    $.each( items, function( index, item ) {
      var li;
      if ( item.department != currentDepartment ) {
        ul.append( "<li class='ui-autocomplete-category'>" + item.department + "</li>" );
        currentDepartment = item.department;
      }
      li = that._renderItemData( ul, item );
      if ( item.department ) {
        li.attr( "aria-label", item.department + " : " + item.course );
      }
    });
  }
});

// autopopulation
$(function() {

  var course_data = $.getJSON("/static/js/mason_courses.json");

  // course_data is an object
  console.log(course_data);
  // yet despite this showing everything in the browser, it is 'undefined'
  // for this below?????
  console.log(course_data.responseText);

  $('#id_course_abbr').on('input', function(e) {
    e.preventDefault();

    $( "#id_course_abbr" ).catcomplete({
      delay: 0,
      source: course_data
    });

  });

});

