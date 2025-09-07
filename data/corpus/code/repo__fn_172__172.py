public function addResponse($key, array $response)
    {
        $originalRequest = isset($this->request[$key]) ? $this->request[$key] : null;
        $responseBody = isset($response['body']) ? $response['body'] : null;
        $responseError = isset($response['error']) ? $response['error'] : null;
        $responseMethod = isset($response['method']) ? $response['method'] : null;

        $this->responses[$key] = new Response($originalRequest, $responseBody, $responseError, $responseMethod);
    }