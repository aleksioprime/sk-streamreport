import { AuthResource } from "@/services/resources/auth.resource";
import { UserResource } from "@/services/resources/general/user.resource";
import { GroupResource } from "@/services/resources/general/group.resource";
import { AcademicYearResource } from "@/services/resources/general/academicYear.resource";
import { ReportPeriodResource } from "@/services/resources/report/reportPeriod.resource";
import { ReportCriterionResource } from "@/services/resources/report/reportCriterion.resource";
import { StudentExtraReportResource } from "@/services/resources/report/studentExtraReport.resource";
import { StudentMentorReportResource } from "@/services/resources/report/studentMentorReport.resource";
import { StudentMentorReportPrimaryResource } from "@/services/resources/report/studentMentorReportPrimary.resource";
import { ReportExtraResource } from "@/services/resources/report/reportExtra.resource";
import { ReportMentorResource } from "@/services/resources/report/reportMentor.resource";
import { ReportMentorPrimaryResource } from "@/services/resources/report/reportMentorPrimary.resource";
import { ReportMentorIbProfileResource } from "@/services/resources/report/reportMentorIbProfile.resource";
import { ReportTeacherPrimaryResource } from "@/services/resources/report/reportTeacherPrimary.resource";
import { ReportTeacherSecondaryResource } from "@/services/resources/report/reportTeacherSecondary.resource";
import { ReportTeacherHighResource } from "@/services/resources/report/reportTeacherHigh.resource";
import { ReportPrimaryTopicResource } from "@/services/resources/report/reportPrimaryTopic.resource";
import { ReportSecondaryCriterionResource } from "@/services/resources/report/reportSecondaryCriterion.resource";
import { ReportSecondaryLevelResource } from "@/services/resources/report/reportSecondaryLevel.resource";
import { ReportTeacherAchievementResource } from "@/services/resources/report/reportTeacherAchievement.resource";
import { StudyYearResource } from "@/services/resources/general/studyYear.resource";
import { SubjectResource } from "@/services/resources/curriculum/subject.resource";
import { CurriculumResource } from "@/services/resources/curriculum/curriculum.resource";
import { CourseResource } from "@/services/resources/syllabus/course.resource";
import { ObjectiveResource } from "@/services/resources/myp/objective.resource";
import { StrandResource } from "@/services/resources/myp/strand.resource";
import { LearnerProfileResource } from "@/services/resources/ibo/learnerProfile.resource";
import { UnitReflectionPostResource } from "@/services/resources/ibo/unitReflectionPost.resource";
import { IbProfileDevelopResource } from "@/services/resources/ibo/ibProfileDevelop.resource";
import { EventParticipationResource } from "@/services/resources/portfolio/eventParticipation.resource";
import { TransdisciplinaryThemeResource } from "@/services/resources/pyp/transdisciplinaryTheme.resource";
import { PypAtlSkillResource } from "@/services/resources/pyp/pypAtlSkill.resource";
import { PypKeyConceptResource } from "@/services/resources/pyp/pypKeyConcept.resource";
import { PypAtlClusterResource } from "@/services/resources/pyp/pypAtlCluster.resource";
import { PypUnitPlannerResource } from "@/services/resources/pyp/pypUnitPlanner.resource";
import { PypAtlDevelopResource } from "@/services/resources/pyp/pypAtlDevelop.resource";
import { PypLinesOfInquiryResource } from "@/services/resources/pyp/pypLinesOfInquiry.resource";
import { PypRelatedConceptResource } from "@/services/resources/pyp/pypRelatedConcept.resource";

export default {
    auth: new AuthResource(),
    user: new UserResource(),
    group: new GroupResource(),
    academicYear: new AcademicYearResource(),
    reportPeriod: new ReportPeriodResource(),
    reportCriterion: new ReportCriterionResource(),
    studentExtraReport: new StudentExtraReportResource(),
    studentMentorReport: new StudentMentorReportResource(),
    studentMentorPrimaryReport: new StudentMentorReportPrimaryResource(),
    reportExtra: new ReportExtraResource(),
    reportMentor: new ReportMentorResource(),
    reportMentorPrimary: new ReportMentorPrimaryResource(),
    reportMentorIbProfile: new ReportMentorIbProfileResource(),
    reportTeacherPrimary: new ReportTeacherPrimaryResource(),
    reportTeacherSecondary: new ReportTeacherSecondaryResource(),
    reportTeacherHigh: new ReportTeacherHighResource(),
    reportPrimaryTopic: new ReportPrimaryTopicResource(),
    reportSecondaryCriterion: new ReportSecondaryCriterionResource(),
    reportSecondaryLevel: new ReportSecondaryLevelResource(),
    reportTeacherAchievement: new ReportTeacherAchievementResource(),
    studyYear: new StudyYearResource(),
    subject: new SubjectResource(),
    curriculum: new CurriculumResource(),
    course: new CourseResource(),
    objective: new ObjectiveResource(),
    strand: new StrandResource(),
    learnerProfile: new LearnerProfileResource(),
    ibProfileDevelop: new IbProfileDevelopResource(),
    unitReflectionPost: new UnitReflectionPostResource(),
    eventParticipation: new EventParticipationResource(),
    pypUnitPlanner: new PypUnitPlannerResource(),
    transdisciplinaryTheme: new TransdisciplinaryThemeResource(),
    pypKeyConcept: new PypKeyConceptResource(),
    pypAtlSkill: new PypAtlSkillResource(),
    pypAtlCluster: new PypAtlClusterResource(),
    pypAtlDevelop: new PypAtlDevelopResource(),
    pypLinesOfInquiry: new PypLinesOfInquiryResource(),
    pypRelatedConcept: new PypRelatedConceptResource(),
  };