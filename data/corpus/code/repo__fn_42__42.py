def create_hparams_from_json(json_path, hparams=None):
  """"""
  tf.logging.info("Loading hparams from existing json %s" % json_path)
  with tf.gfile.Open(json_path, "r") as f:
    hparams_values = json.load(f)
    # Prevent certain keys from overwriting the passed-in hparams.
    # TODO(trandustin): Remove this hack after registries are available to avoid
    # saving them as functions.
    hparams_values.pop("bottom", None)
    hparams_values.pop("loss", None)
    hparams_values.pop("name", None)
    hparams_values.pop("top", None)
    hparams_values.pop("weights_fn", None)
    new_hparams = hparam.HParams(**hparams_values)
    # Some keys are in new_hparams but not hparams, so we need to be more
    #   careful than simply using parse_json() from HParams
    if hparams:  # hparams specified, so update values from json
      for key in sorted(new_hparams.values().keys()):
        if hasattr(hparams, key):  # Overlapped keys
          value = getattr(hparams, key)
          new_value = getattr(new_hparams, key)
          if value != new_value:  # Different values
            tf.logging.info("Overwrite key %s: %s -> %s" % (
                key, value, new_value))
            setattr(hparams, key, new_value)
    else:
      hparams = new_hparams

  return hparams