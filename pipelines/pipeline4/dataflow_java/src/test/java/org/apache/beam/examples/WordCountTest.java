package org.apache.beam.examples;

import java.util.Arrays;
import java.util.List;
import org.apache.beam.examples.WordCount.CountWords;
import org.apache.beam.examples.WordCount.FormatAsTextFn;
import org.apache.beam.sdk.coders.StringUtf8Coder;
import org.apache.beam.sdk.testing.PAssert;
import org.apache.beam.sdk.testing.TestPipeline;
import org.apache.beam.sdk.transforms.Create;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.values.PCollection;
import org.junit.Rule;
import org.junit.Test;

/** Tests of WordCount */
public class WordCountTest {

  static final String[] WORDS_ARRAY =
      new String[] {
        "five", "five four", "five four three", "five four three two", "", "five four three two one"
      };

  static final List<String> WORDS = Arrays.asList(WORDS_ARRAY);

  static final String[] COUNTS_ARRAY =
      new String[] {"five: 5", "four: 4", "three: 3", "two: 2", "one: 1"};
  @Rule public TestPipeline p = TestPipeline.create();

  /** Example test that tests a PTransform by using an in-memory input and inspecting the output. */
  @Test
  public void testCountWords() throws Exception {
    PCollection<String> input = p.apply(Create.of(WORDS).withCoder(StringUtf8Coder.of()));

    PCollection<String> output =
        input.apply(new CountWords()).apply(MapElements.via(new FormatAsTextFn()));

    PAssert.that(output).containsInAnyOrder(COUNTS_ARRAY);
    p.run().waitUntilFinish();
  }
}
