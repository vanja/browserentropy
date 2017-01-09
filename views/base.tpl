<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Web browser entropy</title>
    <!-- Bootstrap -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/custom.css" rel="stylesheet">
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
  </head>
  <body>
    % include('navbar.tpl')
    <div class="container">
      {{!base}}
    </div>
    <footer class="footer">
      <p class="text-center"><small>© 2016</small></p>
    </footer>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    % import config
    % if config.USE_CDN:
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    % else:
    <script src="static/js/jquery.min.js"></script>
    % end
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="static/js/bootstrap.min.js"></script>
    <script>
      $(function () { $('[data-toggle="tooltip"]').tooltip(); })
    </script>
    <script>
      $(document).ready(function(){
        if ($('#fplink').length) {
          $('#fplink').attr('href', '/fp');
        }
      });
    </script>
\\
    % if defined('registered_methods'):
    <!-- Reference embedded fp scripts and templates -->
      % from bottle import template
      % for method in list(filter(lambda m: m.template is not None, registered_methods)):
    {{!''.join(template(method.template, template=template))}}
      % end
      % include('run_scripts.tpl')
    % end
\\
    % if defined('referenced_scripts'):
    <!-- Reference external fp scripts -->
      % import resources
      % for script in resources.referenced_scripts:
    <script src="{{script}}"></script>
      % end
    % end
  </body>
</html>