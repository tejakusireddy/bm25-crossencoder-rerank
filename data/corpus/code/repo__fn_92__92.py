public static function clearCache($postId, $post)
    {
        if (wp_is_post_revision($postId) || get_post_status($postId) != 'publish') {
            return false;
        }

        wp_cache_delete($postId, self::getKeyGroup());
        wp_cache_delete($post->post_type, self::getKeyGroup());

        // Empty post type for all sites in network (?)
        if (function_exists('is_multisite') && is_multisite() && apply_filters('Municipio\Cache\EmptyForAllBlogs', false, $post)) {
            $blogs = get_sites();

            foreach ($blogs as $blog) {
                wp_cache_delete($post->post_type, self::getKeyGroup($blog->blog_id));
            }
        }

        return true;
    }