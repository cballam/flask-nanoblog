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
  console.log(object);
  $.ajax({
        url: "../api/points",
        type: "post",
        data: object,
        success: function (response) {
           console.log("Successfully sent data")
        }
    });
};
