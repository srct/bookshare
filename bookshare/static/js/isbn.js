$(function() {
  $('#id_ISBN').on('input', function(e) {
    e.preventDefault();

    if( ! $('#section-collapse').hasClass('in') ){
      $('#section-collapse').collapse('show');
    }

    var isbn = $('#id_ISBN').val();
    var is_valid = isValidISBN( isbn );

    if( ! is_valid ){
      $('#id_title').val( '' );
      $('#id_author').val( '' );
      $('#id_year').val( '' );
      $('#id_edition').val( '' );
    } else {

      var url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + isbn + "?method=getMetadata&format=json&fl=title,author,year,ed"

      $.ajax({
        dataType: "jsonp",
        url: url,
      }).done( function(data) { process_ISBN_json(data); } );

    }

    if( ! is_valid ) {
      $('#form-group-ISBN').addClass('has-error');
      $('#form-group-ISBN').removeClass('has-success');
    } else {
      $('#form-group-ISBN').removeClass('has-error');
      $('#form-group-ISBN').addClass('has-success');
    }

  });
});


function process_ISBN_json( json ) {

  var title = "No results found.";
  var author = "No results found.";
  var year = "No results found.";
  var edition = "No results found.";

  // There should only ever be a single element, if any.
  if( json.list[0] ){
    title = json.list[0].title;
    author = json.list[0].author;
    year = json.list[0].year;
    edition = json.list[0].ed;
    
  }

  $('#id_title').val( title );
  $('#id_author').val( author );
  $('#id_year').val( year );
  $('#id_edition').val( edition );
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
    var chars = isbn.split('');

    return false;
  }
}
