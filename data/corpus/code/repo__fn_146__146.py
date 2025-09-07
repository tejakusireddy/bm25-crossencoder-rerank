public void parse() {
        Map<String, Disgenet> disgenetMap = new HashMap<>();

        BufferedReader reader;
        try {
            // Disgenet file is usually downloaded as a .tar.gz file
            if (disgenetFilePath.toFile().getName().endsWith("tar.gz")) {
                TarArchiveInputStream tarInput = new TarArchiveInputStream(
                        new GzipCompressorInputStream(new FileInputStream(disgenetFilePath.toFile())));
//                TarArchiveEntry currentEntry = tarInput.getNextTarEntry();
//                BufferedReader br = null;
                reader = new BufferedReader(new InputStreamReader(tarInput)); // Read directly from tarInput
            } else {
                reader = FileUtils.newBufferedReader(disgenetFilePath);
            }
//            if (disgenetFilePath.toFile().getName().endsWith("txt.gz")) {
//                reader = new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(disgenetFilePath.toFile()))));
//            } else {
//                reader = Files.newBufferedReader(disgenetFilePath, Charset.defaultCharset());
//            }

            logger.info("Parsing Disgenet file " + disgenetFilePath + " ...");
            // first line is the header -> ignore it
            reader.readLine();
            long processedDisgenetLines = fillDisgenetMap(disgenetMap, reader);

            logger.info("Serializing parsed variants ...");
            Collection<Disgenet> allDisgenetRecords = disgenetMap.values();
            for (Disgenet disGeNetRecord : allDisgenetRecords) {
                serializer.serialize(disGeNetRecord);
            }
            logger.info("Done");
            this.printSummary(processedDisgenetLines, allDisgenetRecords.size());

        } catch (FileNotFoundException e) {
            logger.error("Disgenet file " + disgenetFilePath + " not found");
        } catch (IOException e) {
            logger.error("Error reading Disgenet file " + disgenetFilePath + ": " + e.getMessage());
        }
    }