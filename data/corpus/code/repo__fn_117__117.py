public void layoutCalendar(Date timeTarget)
    {
        calendar.setTime(timeTarget);
        
        int hour = calendar.get(Calendar.HOUR_OF_DAY);
        int minute = calendar.get(Calendar.MINUTE);
                
        String[] array = new String[24 * 2];
        calendar.set(Calendar.HOUR_OF_DAY, 0);
        calendar.set(Calendar.MINUTE, 0);
        calendar.set(Calendar.SECOND, 0);
        calendar.set(Calendar.MILLISECOND, 0);
        int selectedIndex = -1;
        for (int i = 0; i < array.length; i++)
        {
            if (hour == calendar.get(Calendar.HOUR_OF_DAY))
                if (minute == calendar.get(Calendar.MINUTE))
                    selectedIndex = i;
            Date time = calendar.getTime();
            String strTime = timeFormat.format(time);
            array[i] = strTime;
            calendar.add(Calendar.MINUTE, 30);
        }
        DefaultComboBoxModel model = new DefaultComboBoxModel(array);
        this.setVisibleRowCount(10);
        this.setModel(model);
        if (selectedIndex != -1)
            this.setSelectedIndex(selectedIndex);
    }