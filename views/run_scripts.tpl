% import constants

<script>
  $(document).ready(function () {
    setTimeout(function() {
      var names = Array();
      var requests = Array();

      % for method in registered_methods:
        % if method.js is not None:
      names.push('{{method.runtime_id}}');
      requests.push({{method.js}});
        % end
      % end

      var defer = $.when.apply($, requests).done(function () {
        var results_dict = new Object();
        $.each(arguments, function (index, responseData) {
          results_dict[names[index]] = responseData;
        });

        $.ajax({
          type: "POST",
          url: "/fp",
          data: JSON.stringify({
            {{constants.FP_ROOT}}: results_dict, {{!headers}}
          }),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          converters: {
              'text json': true
          },
          success: function (result) {
            $('.spinner').first().fadeOut(1000, function() {$(this).remove();});
            setTimeout(function() {
                $("#result_placeholder").html(result);
            }, 1000);
          },
          failure: function (errMsg) {
            console.log("ajax post failure: " + errMsg);
          }
        });
      });
    }, 2000);
  });
</script>
