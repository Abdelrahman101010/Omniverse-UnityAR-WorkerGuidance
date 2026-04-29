VUFORIA MODEL TARGET PLACEMENT

Place your Model Target files here before running the automation:

  shared/samples/targets/v1.0.0/Fixture_detectors_1.xml
  shared/samples/targets/v1.0.0/Fixture_detectors_1.dat

Rename your existing Vuforia Model Target .xml/.dat to match
(or pass custom names via --target-xml / --target-dat to automate_job.py).

Once in place, the server will serve them at:
  http://141.43.76.21:8080/api/targets/v1.0.0/Fixture_detectors_1.xml
  http://141.43.76.21:8080/api/targets/v1.0.0/Fixture_detectors_1.dat

The Unity client downloads both BEFORE requesting a job.
