def create_or_update(cls, build):
        

        test_summary = build.test_summary
        metrics_summary = MetricsSummary(build)
        now = timezone.now()
        test_runs_total = build.test_runs.count()
        test_runs_completed = build.test_runs.filter(completed=True).count()
        test_runs_incomplete = build.test_runs.filter(completed=False).count()
        regressions = None
        fixes = None

        previous_build = Build.objects.filter(
            status__finished=True,
            datetime__lt=build.datetime,
            project=build.project,
        ).order_by('datetime').last()
        if previous_build is not None:
            comparison = TestComparison(previous_build, build)
            if comparison.regressions:
                regressions = yaml.dump(comparison.regressions)
            if comparison.fixes:
                fixes = yaml.dump(comparison.fixes)

        finished, _ = build.finished
        data = {
            'tests_pass': test_summary.tests_pass,
            'tests_fail': test_summary.tests_fail,
            'tests_xfail': test_summary.tests_xfail,
            'tests_skip': test_summary.tests_skip,
            'metrics_summary': metrics_summary.value,
            'has_metrics': metrics_summary.has_metrics,
            'last_updated': now,
            'finished': finished,
            'test_runs_total': test_runs_total,
            'test_runs_completed': test_runs_completed,
            'test_runs_incomplete': test_runs_incomplete,
            'regressions': regressions,
            'fixes': fixes
        }

        status, created = cls.objects.get_or_create(build=build, defaults=data)
        if not created and test_summary.tests_total >= status.tests_total:
            # XXX the test above for the new total number of tests prevents
            # results that arrived earlier, but are only being processed now,
            # from overwriting a ProjectStatus created by results that arrived
            # later but were already processed.
            status.tests_pass = test_summary.tests_pass
            status.tests_fail = test_summary.tests_fail
            status.tests_xfail = test_summary.tests_xfail
            status.tests_skip = test_summary.tests_skip
            status.metrics_summary = metrics_summary.value
            status.has_metrics = metrics_summary.has_metrics
            status.last_updated = now
            finished, _ = build.finished
            status.finished = finished
            status.build = build
            status.test_runs_total = test_runs_total
            status.test_runs_completed = test_runs_completed
            status.test_runs_incomplete = test_runs_incomplete
            status.regressions = regressions
            status.fixes = fixes
            status.save()
        return status