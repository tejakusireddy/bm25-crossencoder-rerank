function () {
        var option = clone(this.option);

        each(option, function (opts, mainType) {
            if (ComponentModel.hasClass(mainType)) {
                var opts = modelUtil.normalizeToArray(opts);
                for (var i = opts.length - 1; i >= 0; i--) {
                    // Remove options with inner id.
                    if (modelUtil.isIdInner(opts[i])) {
                        opts.splice(i, 1);
                    }
                }
                option[mainType] = opts;
            }
        });

        delete option[OPTION_INNER_KEY];

        return option;
    }