// Toggles given item
function collapseItem(id){
  $(document).ready(function(){
      $(id).toggle(10);
  });
};

// Sends data to score api
function newScore(score, id){
  object = {
    score: score,
    post_id: id
  };
  $.ajax({
        url: "../api/points",
        type: "post",
        data: object,
        success: function (response) {
          // toggle the button color
           if (score == 1){
             if ($("#" + id + "up").css('background-color') == 'rgb(0, 128, 0)'){
               $("#" + id + "up").css('background-color', "lightgray");
             }
             else {
               $("#" + id + "up").css('background-color', "green");
             }
             $("#" + id + "down").css('background-color', "lightgray");
           }
           else if (score == -1){
             if ($("#" + id + "down").css('background-color') == 'rgb(255, 0, 0)'){
               $("#" + id + "down").css('background-color', "lightgray");
             }
             else {
               $("#" + id + "down").css('background-color', 'red');
             }
             $("#" + id + "up").css('background-color', "lightgray");
           }
        }
    });
};
