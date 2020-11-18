import statistics
from os import environ
from alto_segment_lib.segment import Segment, Line, SegmentGroup
from alto_segment_lib.segment_group_handler import SegmentGroupHandler
from alto_segment_lib.segment_helper import SegmentHelper
from alto_segment_lib.line_extractor.extractor import LineExtractor
environ["OPENCV_IO_ENABLE_JASPER"] = "true"


class SegmentGrouper:

    def group_segments_in_order(self, headers_in: list[Line], paragraphs_in: list[Segment], lines_in: list[Line]):
        segments = paragraphs_in.copy()

        # Find paragraph median
        segment_width = []

        for segment in segments:
            segment_width.append(segment.width())
        paragraph_median = statistics.median(segment_width)

        lines = [element for element, element in enumerate(lines_in) if element.is_horizontal()]

        for header in headers_in:
            segment = Segment()
            segment.type = "heading"
            segment.x1 = header.x1
            segment.x2 = header.x2
            segment.y1 = header.y1
            segment.y2 = header.y2
            segments.append(segment)

        content_bounds = SegmentHelper.get_content_bounds(segments)
        print(content_bounds)

        for line in lines:
            segment = Segment()
            segment.type = "line"
            segment.x1 = line.x1
            segment.x2 = line.x2
            segment.y1 = line.y1
            segment.y2 = line.y2
            segments.append(segment)

        # Sort headers and paragraphs by lowest x, lowest y.
        segments = sorted(segments, key=lambda i: (i.x1, i.y1))


        print(paragraph_median*6)

        print("Found segments: "+str(len(segments)))

        segments_to_check = segments.copy()
        group_handler = SegmentGroupHandler()

        for segment in segments:
            print(segment.type+" on position ("+str(segment.x1)+","+str(segment.y1)+")")

            if segment.type == "heading":
                group_handler.end_group()
                group_handler.start_group()
                group_handler.add_segment(segment)
            elif segment.type == "line":
                ghost_header = group_handler.get_header_segment()

                if ghost_header is not None:
                    print(ghost_header)
                    for sub_segment in segments_to_check:
                        # Find only segments located between the header and the found line.
                        if ghost_header.between_x_coords(sub_segment.x1) and sub_segment.x1 > segment.x2:
                            print(ghost_header)
                            group_handler.add_segment(sub_segment)
                            segments_to_check.remove(sub_segment)
                    group_handler.end_group()
            else:
                group_handler.add_segment(segment)

            # Clean up
            segments_to_check.remove(segment)

        group_handler.finalize()
        return group_handler.groups

