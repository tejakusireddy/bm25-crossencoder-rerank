def check_symbol_to_proc
      return unless method_call.block_argument_names.count == 1
      return if method_call.block_body.nil?
      return unless method_call.block_body.sexp_type == :call
      return if method_call.arguments.count > 0

      body_method_call = MethodCall.new(method_call.block_body)

      return unless body_method_call.arguments.count.zero?
      return if body_method_call.has_block?
      return unless body_method_call.receiver.name == method_call.block_argument_names.first

      add_offense(:block_vs_symbol_to_proc)
    end