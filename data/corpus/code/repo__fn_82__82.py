public function modal_template() {

		$output = '<script type="text/html" id="' . esc_attr( $this->id() ) . '-components">';
		foreach ( $this->modals as $modal ) {

			$label         = $modal->struct['label'];
			$data          = $modal->get_data();
			$data_template = $this->drill_in( $data[ $modal->slug ], '{{@root' );
			$modal->set_data( array( $modal->slug => $data_template ) );

			$modal->render();

			$setup = null;
			if ( count( $modal->child ) > 1 ) {
				$setup = ' data-setup="true" ';
			}

			$output .= '<button type="button" class="button uix-component-trigger" style="margin:12px 0 0 12px;" data-label="' . esc_attr( $modal->attributes['data-title'] ) . '" data-type="' . $modal->slug . '" ' . $setup . ' data-id="' . esc_attr( $modal->id() ) . '">' . $label . '</button> ';

		}
		$output .= '</script>';

		return $output;
	}