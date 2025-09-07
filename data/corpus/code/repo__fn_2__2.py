function() {
        var options = this.options;

        if (options.hideOthers) {
            this.secondary.each(function() {
                var sidebar = $(this);

                if (sidebar.hasClass('is-expanded')) {
                    sidebar.toolkit('offCanvas', 'hide');
                }
            });
        }

        this.fireEvent('showing');

        this.container.addClass('move-' + this.opposite);

        this.element
            .reveal()
            .addClass('is-expanded')
            .aria('expanded', true);

        if (options.stopScroll) {
            $('body').addClass('no-scroll');
        }

        this.fireEvent('shown');
    }