public static function export_customfield_data(data_controller $data, array $subcontext) {
        $context = $data->get_context();

        $exportdata = $data->to_record();
        $exportdata->fieldtype = $data->get_field()->get('type');
        $exportdata->fieldshortname = $data->get_field()->get('shortname');
        $exportdata->fieldname = $data->get_field()->get_formatted_name();
        $exportdata->timecreated = \core_privacy\local\request\transform::datetime($exportdata->timecreated);
        $exportdata->timemodified = \core_privacy\local\request\transform::datetime($exportdata->timemodified);
        unset($exportdata->contextid);
        // Use the "export_value" by default for the 'value' attribute, however the plugins may override it in their callback.
        $exportdata->value = $data->export_value();

        $classname = manager::get_provider_classname_for_component('customfield_' . $data->get_field()->get('type'));
        if (class_exists($classname) && is_subclass_of($classname, customfield_provider::class)) {
            component_class_callback($classname, 'export_customfield_data', [$data, $exportdata, $subcontext]);
        } else {
            // Custom field plugin does not implement customfield_provider, just export default value.
            writer::with_context($context)->export_data($subcontext, $exportdata);
        }
    }