public function downloadFeedItem(models\Download\Feed\DownloadFeedItem $DownloadFeedItem)
    {
        $service = sprintf(self::API_DOWNLOAD_FEEDS_ITEMS_ITEM_DOWNLOAD, $DownloadFeedItem->getFeedId(), $DownloadFeedItem->getId());
        $rest    = $this->callService('POST', $service, $DownloadFeedItem);

        return $rest->getSuccess();
    }