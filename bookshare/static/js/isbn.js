$(function() {

  // add input handler
  $('#id_ISBN').on('input', function(e) {
    e.preventDefault();

    // if the section is already hidden, show it
    if( ! $('#section-collapse').hasClass('in') ){
      $('#section-collapse').collapse('show');
    }

    // grab and validate the ISBN
    var isbn = $('#id_ISBN').val();
    var is_valid = isValidISBN( isbn );

    // Style the form appropriately.
    if( ! is_valid ) {
      $('#form-group-ISBN').addClass('has-error');
      $('#form-group-ISBN').removeClass('has-success');
    } else {
      $('#form-group-ISBN').removeClass('has-error');
      $('#form-group-ISBN').addClass('has-success');
    }

    if( ! is_valid ){ // If invalid, clear the form.
      $('#id_title').val( '' );
      $('#id_author').val( '' );
      $('#id_year').val( '' );
      $('#id_edition').val( '' );
    } else { // Otherwise, poll worldcat for data.

      var url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + isbn + "?method=getMetadata&format=json&fl=title,author,year,ed"

      $.ajax({
        dataType: "jsonp",
        url: url,
      }).done( function(data) { process_ISBN_json(data); } );

    }

  });
});


// This function takes a JSON response object and grabs the fields from it,
// spitting them into the form fields.
function process_ISBN_json( json ) {
  // There should only ever be a single element, if any.
  if( json.stat == "ok" ){
    title = json.list[0].title;
    author = json.list[0].author;
    year = json.list[0].year;
    edition = json.list[0].ed;

    $('#id_title').val( title );
    $('#id_author').val( author );
    $('#id_year').val( year );
    $('#id_edition').val( edition );
  }
}


function isValidISBN (isbn) { 
  isbn = isbn.replace(/[^\dX]/gi, ''); 

  if(isbn.length != 10 && isbn.length != 13){
    return false;
  }

  if(isbn.length == 10){ 
    var chars = isbn.split(''); 
    if(chars[9].toUpperCase() == 'X'){ 
      chars[9] = 10; 
    } 
    var sum = 0; 
    for (var i = 0; i < chars.length; i++) { 
      sum += ((10-i) * parseInt(chars[i])); 
    }; 
    return ((sum % 11) == 0); 
  }
  
  if(isbn.length == 13){
    var check, i;

    check = 0;
    for( i = 0; i < 13; i += 2 ){
      check += parseInt(isbn.charAt(i));
    }
    for( i = 1; i < 12; i += 2 ){
      check += 3 * parseInt(isbn.charAt(i));
    }

    return check % 10 === 0;
  }
}
