// Toggles given item
function collapseItem(id){
  $(document).ready(function(){
      $(id).toggle(10);
  });
};

// Sends data to score api
function newScore(score, comment_id, post_id){
  object = {
    score: score,
    comment_id: comment_id,
    post_id: post_id
  };
  $.ajax({
        url: "../api/points",
        type: "post",
        data: object,
        success: function (response) {
          // Create type object to hold values needed to change button color
          let type = null;
          if (object.comment_id !== null) {
            type = [comment_id, "up", "down"]
          }
          else {
            type = [post_id ,"upPOST", "downPOST"]
          }
          // Button color toggling logic
           if (score == 1){
             if ($("#" + type[0] + type[1]).css('background-color') == 'rgb(0, 128, 0)'){
               $("#" +type[0]+ type[1]).css('background-color', "lightgray");
             }
             else {
               $("#" +type[0]+ type[1]).css('background-color', "green");
             }
             $("#" +type[0]+ type[2]).css('background-color', "lightgray");
           }
           else if (score == -1){
             if ($("#" +type[0]+ type[2]).css('background-color') == 'rgb(255, 0, 0)'){
               $("#" +type[0]+ type[2]).css('background-color', "lightgray");
             }
             else {
               $("#" +type[0]+ type[2]).css('background-color', 'red');
             }
             $("#" +type[0]+ type[1]).css('background-color', "lightgray");
           }
        }
    });
};
