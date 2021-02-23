#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to check for DICOM fields with PHI in an XNAT project - April 2020 
#
# Usage: edit input_path and run from the server where the images are stored

import pydicom
import os, sys 
import fnmatch

# ---------------------------------------------------------------------------------------------------------------------

# Updated 2021: http://dicom.nema.org/medical/dicom/current/output/html/part15.html#table_E.1-1

list_phi = ['AccessionNumber','AcquisitionComments','AcquisitionContextSequence','AcquisitionDate','AcquisitionDateTime',
            'AcquisitionDeviceProcessingDescription','AcquisitionFieldOfViewLabel','AcquisitionProtocolDescription',
            'AcquisitionTime','ActualHumanPerformersSequence','AdditionalPatientHistory','Address','AddressTrial',
            'AdmissionID','AdmittingDate','AdmittingDiagnosesCodeSequence','AdmittingDiagnosesDescription','AdmittingTime',
            'AffectedSOPInstanceUID','Allergies','Arbitrary','AuthorObserverSequence','BarcodeValue','BeamDescription',
            'BolusDescription','BranchOfService','CameraOwnerName','CassetteID','ClinicalTrialCoordinatingCenterName',
            'ClinicalTrialProtocolEthicsCommitteeApprovalNumber','ClinicalTrialProtocolEthicsCommitteeName',
            'ClinicalTrialProtocolID','ClinicalTrialProtocolName','ClinicalTrialSeriesDescription','ClinicalTrialSeriesID',
            'ClinicalTrialSiteID','ClinicalTrialSiteName','ClinicalTrialSponsorName','ClinicalTrialSubjectID',
            'ClinicalTrialSubjectReadingID','ClinicalTrialTimePointDescription','ClinicalTrialTimePointID',
            'CommentsonRadiationDose','CommentsonthePerformedProcedureStep','CompensatorDescription','ConcatenationUID',
            'ConceptualVolumeCombinationDescription','ConceptualVolumeDescription','ConceptualVolumeUID',
            'ConfidentialityConstraintonPatientDataDescription','ConstituentConceptualVolumeUID',
            'ConsultingPhysicianName','ConsultingPhysicianIdentificationSequence','ContainerComponentID','ContainerDescription',
            'ContainerIdentifier','ContentCreatorIdentificationCodeSequence','ContentCreatorName','ContentDate','ContentSequence',
            'ContentTime','ContrastBolusAgent','ContributionDescription','CountryOfResidence','CurrentObserver','CurrentObserverTrial',
            'CurrentPatientLocation','CurveData','CurveDate','CurveTime','CustodialOrganizationSequence','DataSetTrailingPadding',
            'DecompositionDescription','DerivationDescription','DetectorID','DeviceAlternateIdentifier','DeviceDescription',
            'DeviceLabel','DeviceSerialNumber','DeviceSettingDescription','DeviceUID','DigitalSignaturesSequence','DigitalSignatureUID',
            'DimensionOrganizationUID','DischargeDiagnosisDescription','DistributionAddress','DistributionName','DoseReferenceDescription',
            'DoseReferenceUID','DosimetricObjectiveUID','EndAcquisitionDateTime','EntityDescription','EntityLabel','EntityLongLabel',
            'EntityName','EquipmentFrameOfReferenceDescription','EthnicGroup','ExpectedCompletionDateTime','FailedSOPInstanceUIDList',
            'FiducialUID','FillerOrderNumberImagingServiceRequest','FirstTreatmentDate','FixationDeviceDescription','FlowIdentifier',
            'FlowIdentifierSequence','FractionationNotes','FractionGroupDescription','FrameComments','FrameOfReferenceUID',
            'FrameOriginTimestamp','GantryID','GeneratorID','GPSAltitude','GPSAltitudeRef','GPSAreaInformation','GPSDateStamp',
            'GPSDestBearing','GPSDestBearingRef','GPSDestDistance','GPSDestDistanceRef','GPSDestLatitude','GPSDestLatitudeRef',
            'GPSDestLongitude','GPSDestLongitudeRef','GPSDifferential','GPSDOP','GPSImgDirection','GPSImgDirectionRef','GPSLatitude',
            'GPSLatitudeRef','GPSLongitude','GPSLongitudeRef','GPSMapDatum','GPSMeasureMode','GPSProcessingMethod','GPSSatellites',
            'GPSSpeed','GPSSpeedRef','GPSStatus','GPSTimeStamp','GPSTrack','GPSTrackRef','GPSVersionID','GraphicAnnotationSequence',
            'HumanPerformerName','HumanPerformerOrganization','IconImageSequence','IdentifyingComments','ImageComments',
            'ImagePresentationComments','ImagingServiceRequestComments','ImpedanceMeasurementDateTime','Impressions',
            'InstanceCoercionDateTime','InstanceCreatorUID','InstanceOriginStatus','InstitutionAddress','InstitutionalDepartmentName',
            'InstitutionalDepartmentTypeCodeSequence','InstitutionCodeSequence','InstitutionName','InsurancePlanIdentification',
            'IntendedPhaseEndDate','IntendedPhaseStartDate','IntendedRecipientsOfResultsIdentificationSequence','InterlockDateTime',
            'InterlockDescription','InterlockOriginDescription','InterpretationApproverSequence','InterpretationAuthor',
            'InterpretationDiagnosisDescription','InterpretationIDIssuer','InterpretationRecorder','InterpretationText',
            'InterpretationTranscriber','IrradiationEventUID','IssuerOfAdmissionID','IssuerOfAdmissionIDSequence','IssuerOfPatientID',
            'IssuerOfServiceEpisodeID','IssuerOfServiceEpisodeIDSequence','IssuerOftheContainerIdentifierSequence','IssuerOftheSpecimenIdentifierSequence',
            'LabelText','LargePaletteColorLookupTableUID','LastMenstrualDate','LensMake','LensModel','LensSerialNumber',
            'LensSpecification','LongDeviceDescription','MAC','MakerNote','ManufacturerDeviceClassUID','ManufacturerDeviceIdentifier',
            'MediaStorageSOPInstanceUID','MedicalAlerts','MedicalRecordLocator','MilitaryRank','ModifiedAttributesSequence',
            'ModifiedImageDescription','ModifyingDeviceID','MostRecentTreatmentDate','MultienergyAcquisitionDescription',
            'MultiplexGroupUID','NameOfPhysiciansReadingStudy','NamesOfIntendedRecipientsOfResults','NonconformingModifiedAttributesSequence',
            'NonconformingDataElementValue','ObservationDateTrial','ObservationDate','ObservationSubjectUIDTrial','ObservationSubjectUID',
            'ObservationTimeTrial','ObservationTime','ObservationUID','Occupation','OperatorIdentificationSequence','OperatorsName',
            'OrderCallbackPhoneNumber','OrderCallbackTelecomInformation','OrderEnteredBy','OrderEntererLocation','OriginalAttributesSequence',
            'OtherPatientIDs','OtherPatientIDsSequence','OtherPatientNames','OverlayComments','OverlayData','OverlayDate',
            'OverlayTime','OverrideDateTime','PaletteColorLookupTableUID','ParticipantSequence','PatientAddress','PatientAge',
            'PatientBirthDate','PatientBirthName','PatientBirthTime','PatientInstitutionResidence','PatientInsurancePlanCodeSequence',
            'PatientMotherBirthName','PatientName','PatientPrimaryLanguageCodeSequence','PatientPrimaryLanguageModifierCodeSequence',
            'PatientReligiousPreference','PatientSex','PatientSexNeutered','PatientSize','PatientTelecomInformation',
            'PatientTelephoneNumbers','PatientWeight','PatientComments','PatientID','PatientSetupUID','PatientState',
            'PatientTransportArrangements','PerformedLocation','PerformedProcedureStepDescription','PerformedProcedureStepEndDate',
            'PerformedProcedureStepEndDateTime','PerformedProcedureStepEndTime','PerformedProcedureStepID','PerformedProcedureStepStartDate',
            'PerformedProcedureStepStartDateTime','PerformedProcedureStepStartTime','PerformedStationAETitle','PerformedStationGeographicLocationCodeSequence',
            'PerformedStationName','PerformedStationNameCodeSequence','PerformingPhysicianName','PerformingPhysicianIdentificationSequence',
            'PersonAddress','PersonTelecomInformation','PersonTelephoneNumbers','PersonIdentificationCodeSequence','PersonName',
            'PhysicianApprovingInterpretation','PhysiciansOfRecord','PhysiciansOfRecordIdentificationSequence',
            'PhysiciansReadingStudyIdentificationSequence','PlacerOrderNumberImagingServiceRequest','PlateID','PregnancyStatus',
            'PreMedication','PrescriptionDescription','PrescriptionNotes','PrescriptionNotesSequence','PresentationDisplayCollectionUID',
            'PresentationSequenceCollectionUID','PriorTreatmentDoseDescription','Privateattributes','ProcedureStepCancellationDateTime',
            'ProtocolName','RadiationDoseIdentificationLabel','RadiationDoseInVivoMeasurementLabel','RadiationGenerationModeDescription',
            'RadiationGenerationModeLabel','ReasonforOmissionDescription','ReasonforRequestedProcedureCodeSequence','ReasonforStudy',
            'ReasonforSuperseding','ReasonfortheImagingServiceRequest','ReasonfortheRequestedProcedure','ReasonforVisit',
            'ReasonforVisitCodeSequence','RecordedRTControlPointDateTime','ReferencedConceptualVolumeUID','ReferencedDigitalSignatureSequence',
            'ReferencedDoseReferenceUID','ReferencedDosimetricObjectiveUID','ReferencedFiducialsUID','ReferencedFrameOfReferenceUID',
            'ReferencedGeneralPurposeScheduledProcedureStepTransactionUID','ReferencedImageSequence','ReferencedObservationUIDTrial',
            'ReferencedObservationUID','ReferencedPatientAliasSequence','ReferencedPatientPhotoSequence','ReferencedPatientSequence',
            'ReferencedPerformedProcedureStepSequence','ReferencedSOPInstanceMACSequence','ReferencedSOPInstanceUID','ReferencedSOPInstanceUIDinFile',
            'ReferencedStudySequence','ReferringPhysicianAddress','ReferringPhysicianName','ReferringPhysicianTelephoneNumbers',
            'ReferringPhysicianIdentificationSequence','RegionOfResidence','RelatedFrameOfReferenceUID','RequestAttributesSequence',
            'RequestedContrastAgent','RequestedProcedureComments','RequestedProcedureDescription','RequestedProcedureID',
            'RequestedProcedureLocation','RequestedSeriesDescription','RequestedSOPInstanceUID','RequestingPhysician',
            'RequestingService','RespiratoryMotionCompensationTechniqueDescription','ResponsibleOrganization','ResponsiblePerson',
            'ResultsComments','ResultsDistributionListSequence','ResultsIDIssuer','ReviewerName','ROIDescription','ROIGenerationDescription',
            'ROIInterpreter','ROIName','ROIObservationDescription','ROIObservationLabel','RTAccessoryDeviceSlotID','RTAccessoryHolderSlotID',
            'RTPhysicianIntentNarrative','RTPlanDate','RTPlanDescription','RTPlanLabel','RTPlanName','RTPlanTime','RTPrescriptionLabel',
            'RTToleranceSetLabel','RTTreatmentApproachLabel','RTTreatmentPhaseUID','ScheduledHumanPerformersSequence',
            'ScheduledPatientInstitutionResidence','ScheduledPerformingPhysicianName','ScheduledPerformingPhysicianIdentificationSequence',
            'ScheduledProcedureStepDescription','ScheduledProcedureStepEndDate','ScheduledProcedureStepEndTime',
            'ScheduledProcedureStepExpirationDateTime','ScheduledProcedureStepID','ScheduledProcedureStepLocation',
            'ScheduledProcedureStepModificationDateTime','ScheduledProcedureStepStartDate','ScheduledProcedureStepStartDateTime',
            'ScheduledProcedureStepStartTime','ScheduledStationAETitle','ScheduledStationGeographicLocationCodeSequence',
            'ScheduledStationName','ScheduledStationNameCodeSequence','ScheduledStudyLocation','ScheduledStudyLocationAETitle',
            'SeriesDate','SeriesDescription','SeriesInstanceUID','SeriesTime','ServiceEpisodeDescription','ServiceEpisodeID',
            'SetupTechniqueDescription','ShieldingDeviceDescription','SlideIdentifier','SmokingStatus','SOPInstanceUID',
            'SourceConceptualVolumeUID','SourceEndDateTime','SourceIdentifier','SourceImageSequence','SourceManufacturer',
            'SourceSerialNumber','SourceStartDateTime','SpecialNeeds','SpecimenAccessionNumber','SpecimenDetailedDescription',
            'SpecimenIdentifier','SpecimenPreparationSequence','SpecimenShortDescription','SpecimenUID','StartAcquisitionDateTime',
            'StationName','StorageMediaFileSetUID','StructureSetDate','StructureSetDescription','StructureSetLabel','StructureSetName',
            'StructureSetTime','StudyComments','StudyDate','StudyDescription','StudyID','StudyIDIssuer','StudyInstanceUID',
            'StudyTime','SynchronizationFrameOfReferenceUID','TargetUID','TelephoneNumberTrial','TelephoneNumber',
            'TemplateExtensionCreatorUID','TemplateExtensionOrganizationUID','TextComments','TextString','TimezoneOffsetFromUTC',
            'TopicAuthor','TopicKeywords','TopicSubject','TopicTitle','TrackingUID','TransactionUID','TransducerIdentificationSequence',
            'TreatmentDate','TreatmentMachineName','TreatmentPositionGroupLabel','TreatmentPositionGroupUID','TreatmentSessionUID',
            'TreatmentSite','TreatmentTechniqueNotes','TreatmentTime','TreatmentToleranceViolationDateTime','TreatmentToleranceViolationDescription',
            'UDISequence','UID','UniqueDeviceIdentifier','UserContentLabel','UserContentLongLabel','VerbalSourceTrial',
            'VerbalSource','VerbalSourceIdentifierCodeSequenceTrial','VerbalSourceIdentifierCodeSequence','VerifyingObserverIdentificationCodeSequence',
            'VerifyingObserverName','VerifyingObserverSequence','VerifyingOrganization','VisitComments','XRayDetectorID',
            'XRayDetectorLabel','XRaySourceID']


# ---------------------------------------------------------------------------------------------------------------------

list_odds = ['localizer', 'report', 'presentation', 'screen', 'aqnet', 'exam', 'protocol', 'manual', 'mindways', 'vrt', 'manipulated',
             'result', 'reading', 'csamanipulated', 'tab', 'dnrg', 'snrg', 'mpr', 'enhancement', 'secondary', 'other']


# ---------------------------------------------------------------------------------------------------------------------

def check_reports(input_dicom):
    try:     
        data = pydicom.dcmread(input_dicom)

        try:
            image_type = data.ImageType
        except:
            print ('ATTN! No image type in %s!' %input_dicom)
            image_type = '' 
        try:
            series_description = data.SeriesDescription.lower()
        except:
            series_description = ''

        try:
            study_description = data.StudyDescription.lower()
        except:
            study_description = ''

        for odd in list_odds:
            found_odd_image_type = False
            for i in range(len(image_type)):
                image_type_field = data.ImageType[i].lower()
                if (odd in image_type_field):
                    found_odd_image_type = True

            if (found_odd_image_type):        
                print ('ATTN! %s in file %s' % (data.ImageType, input_dicom))
            if (odd in series_description):
                print ('ATTN! %s in file %s' % (series_description, input_dicom))
            if (odd in study_description):
                print ('ATTN! %s in file %s' % (study_description, input_dicom))
            
    except:
        print('No metadata for %s' % input_dicom)

# ---------------------------------------------------------------------------------------------------------------------   

def check_phi(metadata):
    for field in list_phi:
         try: 
            value = metadata[field].value
            if (value != ''):
                print('   - Found %s = %s' %(field, value))
         except:
             pass

# ---------------------------------------------------------------------------------------------------------------------   

def check_private(metadata):
    for key in metadata:
        if (('Private' in key.description()) or ('private' in key.description()) or ('PRIVATE' in key.description())):
            print(key)

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    input_path = '/path/to/DICOM/'
    sessions   = []
    arguments   = sys.argv[1:]
    if (len(arguments) > 0):
        input_list  = arguments[0]
        with open(input_list, mode='r') as input_file:
            line = input_file.readline()
            while line:
                this_session = line.strip()
                sessions.append(this_session)
                line = input_file.readline()
    else:
        sessions = os.listdir(input_path)

    print(len(sessions))

    for session in sessions:
        print('**************')
        print('Session = %s' %(session))
        session_id = session

        # Each subdirectory is a different scan i.e. session                                                                                         
        session_path = input_path + os.sep + session 
        for dirpaths, dirnames, filenames in os.walk(session_path):
            n_dicom = 0
            for filename in filenames:
                if(not ('DS_Store' in filename)):
                    n_dicom = n_dicom + 1
                    dicom_file = os.path.join(dirpaths, filename)
                    check_reports(dicom_file)
                    metadata = pydicom.dcmread(dicom_file)
                    check_phi(metadata)
                    check_private(metadata)
                    # NOTE: This option checks every DICOM file individually 
