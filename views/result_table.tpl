% import result_generator
% alert, message = result_generator.alert_message(fp)
<div class="text-center alert alert-{{alert}}" role="alert">{{message}}</div>

<div id="fp_tables">
% for properties, fpm_name in result_generator.fp_results(fp):
<table class="table table-condensed table-hover table-responsive">
  <caption>{{fpm_name}}</caption>
  <thead>
    <tr>
      <th class="col-sm-3">Property</th>
      <th class="col-sm-7">Value</th>
      <th class="col-sm-1 text-right">
        <a data-toggle="tooltip" title="lower value means more identifiable">Similarity</a>
      </th>
      <th class="col-sm-1 text-right">
        <a data-toggle="tooltip" title="higher value means more identifiable">Entropy</a>
      </th>
    </tr>
  </thead>
  <tbody>
    % for (prop_desc, prop_value, (uniqueness, entropy, percentage)) in properties:
    <tr>
        <td>{{prop_desc}}</td>
        <td class="res-val">{{!prop_value}}</td>
        <td class="text-right">
          <a data-toggle="tooltip" data-placement="left" title="1 in {{uniqueness}} browsers share this value">{{percentage}}%</a>
        </td>
        <td class="text-right">{{entropy}}</td>
    </tr>
    % end
  </tbody>
</table>
<br/>
% end
</div>
<script>
  $(function() { $('[data-toggle="tooltip"]').tooltip() })
</script>

% if defined('no_js') and no_js:
  % rebase('base.tpl')