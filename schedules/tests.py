from django.test import TestCase
from schedules.models import Gap
from users.models import User


# Create your tests here.
class GapTestCase(TestCase):
    # def setUp(self):


    def test_gap_creates_successfully(self):
        gap = Gap()
        self.assertEqual(type(gap), Gap)

    def test_gap_cross_different_days(self):
        gap1 = Gap(start_hour_weekday="1", start_hour='090', end_hour='130')
        gap2 = Gap(start_hour_weekday="2", start_hour='090', end_hour='130')

        sharedGap = gap1.cross(gap2)
        self.assertEqual(sharedGap, None)

    def test_gap_cross_not_overlapping(self):
        gap1 = Gap(start_hour_weekday="1", start_hour='090', end_hour='130')
        gap2 = Gap(start_hour_weekday="1", start_hour='140', end_hour='153')

        sharedGap = gap1.cross(gap2)
        self.assertEqual(sharedGap, None)

    def test_gap_cross_overlapping_case_1(self):
        """
        Case 1: Gaps are overlapped but not contained
        """
        gap1 = Gap(start_hour_weekday="1", start_hour='083', end_hour='113')
        gap2 = Gap(start_hour_weekday="1", start_hour='100', end_hour='130')
        sharedGap = gap1.cross(gap2)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap1.end_hour)

        sharedGap = gap2.cross(gap1)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap1.end_hour)

    def test_gap_cross_overlapping_case_2(self):
        """
        Case 2: One gap is contained in the other
        """
        gap1 = Gap(start_hour_weekday="1", start_hour='083', end_hour='153')
        gap2 = Gap(start_hour_weekday="1", start_hour='100', end_hour='130')
        sharedGap = gap1.cross(gap2)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap2.end_hour)

        sharedGap = gap2.cross(gap1)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap2.end_hour)

    def test_gap_cross_overlapping_case_3(self):
        """
        Case 3: Gaps are exactly contained in each other
        """
        gap1 = Gap(start_hour_weekday="1", start_hour='100', end_hour='170')
        gap2 = Gap(start_hour_weekday="1", start_hour='100', end_hour='170')
        sharedGap = gap1.cross(gap2)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap2.end_hour)

        sharedGap = gap2.cross(gap1)

        self.assertEqual(sharedGap.start_hour, gap2.start_hour)
        self.assertEqual(sharedGap.end_hour, gap2.end_hour)


class GapUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="test", firstNames="user", lastNames="lastUser")

    def test_gap_creates_schedule_updated_on_correct(self):
        # print("UPDATED_ON" + str(self.user.updated_on))
        # print("SCHEDULE_UPDATED_ON" + str(self.user.schedule_updated_on))
        gap = Gap.objects.create(user=self.user)
        # print("UPDATED_ON" + str(self.user.updated_on))
        # print("SCHEDULE_UPDATED_ON" + str(self.user.schedule_updated_on))
        self.assertEqual(self.user.schedule_updated_on, gap.updated_on)
