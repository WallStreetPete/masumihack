"use client";

import { Scale } from "lucide-react";
import { useState, useEffect } from "react";
import { useSendEmails } from "@/hooks/useSendEmails";
import type { Campaign, Email, Prospect } from "../globals/type";
import { Navbar } from "@/components/layout/Navbar";
import { CampaignSidebar } from "@/components/sidebar/CampaignSidebar";
import { AudienceSearch } from "@/components/audience/AudienceSearch";
import { EmptyState } from "@/components/empty/EmptyState";
import { GeneratedEmails } from "@/components/email/GeneratedEmails";
import { EmailTemplate } from "@/components/email/EmailTemplate";
import { ProspectList } from "@/components/prospects/ProspectList";
import { MessagesPanel } from "@/components/messages/MessagesPanel";
import { useGetCampaigns } from "@/hooks/useGetCampaigns";
import { useSearchProspects } from "@/hooks/useSearchProspects";
import { ProspectStackList } from "@/components/prospects";
import { useGenerateEmails } from "@/hooks/useGenerateEmails";
import { ProspectProgress } from "@/components/ui/ProspectProgress";
import { EmailProgress } from "@/components/ui/EmailProgress";

export default function Home() {
  // Progress bar state for ProspectProgress
  const [progressStep, setProgressStep] = useState(0); // 0: looking, 1: formatting, 2: complete
  const [progressValue, setProgressValue] = useState(0);
  const sendEmails = useSendEmails();
  const [isEmpty, setIsEmpty] = useState(true);
  const [description, setDescription] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [emailTemplate, setEmailTemplate] = useState("");
  const [isGeneratingEmails, setIsGeneratingEmails] = useState(false);
  const [showEmailEditor, setShowEmailEditor] = useState<number | null>(null);
  const [selectedProspects, setSelectedProspects] = useState<Prospect[]>([]);
  const [emailTone, setEmailTone] = useState("auto");
  const [emailLength, setEmailLength] = useState("auto");
  const [emailStyle, setEmailStyle] = useState("auto");
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [showCampaign, setShowCampaign] = useState(false);
  const [showGeneratedEmails, setShowGeneratedEmails] = useState(false);
  const [showProspectsList, setShowProspectsList] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign>();
  const [generatedEmailsProspects, setGeneratedEmailsProspects] = useState<
    Prospect[]
  >([]);
  const [createdCampaignTitle, setCreatedCampaignTitle] = useState("");

  const [showMessagesView, setShowMessagesView] = useState(false);
  const [selectedProspectId, setSelectedProspectId] = useState<number | null>(
    null
  );
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [emailProgress, setEmailProgress] = useState(0);
  const [selectedCampaignId, setSelectedCampaignId] = useState<number | null>(
    null
  );

  const searchProspectsHook = useSearchProspects();
  const generateEmails = useGenerateEmails();

  // Fetch campaigns from API and log results
  const getCampaigns = useGetCampaigns();

  useEffect(() => {
    getCampaigns().then((data: Campaign[]) => {
      console.log(data);
      setCampaigns(data);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getProspectName = (id: string | null) => {
    const p = prospects.find((x: Prospect) => x.linkedinUrl === id);
    return p ? p.firstName + " " + p.lastName : "";
  };

  const handleSendEmails = async () => {
    const payload: Campaign = {
      title: createdCampaignTitle,
      prospects: generatedEmailsProspects,
    };

    window.scrollTo({ top: 0, behavior: "smooth" });

    sendEmails(payload).then(() => {
      reset();
      setShowMessagesView(true);
      getCampaigns().then((data: Campaign[]) => {
        setCampaigns(data);
      });
      setSelectedCampaign(payload);
      setSelectedProspectId(0);
      setShowCampaign(true);
      setSelectedCampaignId(0);
    });
  };

  const searchProspects = async () => {
    if (!description.trim()) return;

    setIsLoading(true);
    setProgressStep(0);
    setProgressValue(0);
    let progress = 0;

    // Initial progress up to 30%
    const initialInterval = setInterval(() => {
      if (progress < 30) {
        progress += Math.random() * 2 + 0.5; // slower increment
        setProgressValue(Math.min(progress, 30));
      }
    }, 200); // longer interval

    // Middle progress from 30% to 60%
    const middleInterval = setInterval(() => {
      if (progress >= 30 && progress < 60) {
        progress += Math.random() * 0.8 + 0.2; // slower increment
        setProgressValue(Math.min(progress, 60));
      }
    }, 300); // longer interval

    // Slow progress from 60% to 90%
    const slowInterval = setInterval(() => {
      if (progress >= 60 && progress < 90) {
        progress += Math.random() * 0.4 + 0.1; // slower increment
        setProgressValue(Math.min(progress, 90));
      }
    }, 400); // longer interval

    try {
      const data = await searchProspectsHook(description);

      // Clear all intervals
      [initialInterval, middleInterval, slowInterval].forEach(clearInterval);

      // Final sprint to 100%
      const finalInterval = setInterval(() => {
        progress += 2;
        setProgressValue(Math.min(progress, 100));

        if (progress >= 100) {
          clearInterval(finalInterval);

          // Show results after a brief delay
          setTimeout(() => {
            setIsLoading(false);
            setProspects(data.prospects || []);
            setShowProspectsList(true);
            setSelectedProspects(data.prospects || []);
            setIsCreating(false);
            setCreatedCampaignTitle(data.campaignTitle);
          }, 1000);
        }
      }, 30);
    } catch (error) {
      // Clear all intervals on error
      [initialInterval, middleInterval, slowInterval].forEach(clearInterval);

      setProspects([]);
      setIsLoading(false);
      setIsEmpty(false);
      setProgressStep(0);
      setProgressValue(0);
    }
  };

  const handleExampleClick = (example: string) => {
    setDescription(example);
  };

  // ...other code...

  const handleGenerateEmails = async () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    setIsGeneratingEmails(true);
    setEmailProgress(0);
    let progress = 0;

    // Initial progress up to 30%
    const initialInterval = setInterval(() => {
      if (progress < 30) {
        progress += Math.random() * 2 + 0.5;
        setEmailProgress(Math.min(progress, 30));
      }
    }, 200);

    // Middle progress from 30% to 60%
    const middleInterval = setInterval(() => {
      if (progress >= 30 && progress < 60) {
        progress += Math.random() * 0.8 + 0.2;
        setEmailProgress(Math.min(progress, 60));
      }
    }, 300);

    // Slow progress from 60% to 90%
    const slowInterval = setInterval(() => {
      if (progress >= 60 && progress < 90) {
        progress += Math.random() * 0.4 + 0.1;
        setEmailProgress(Math.min(progress, 90));
      }
    }, 400);

    try {
      const campaign = await generateEmails({ prospects: selectedProspects });
      // Clear all intervals
      [initialInterval, middleInterval, slowInterval].forEach(clearInterval);
      // Final sprint to 100%
      const finalInterval = setInterval(() => {
        progress += 2;
        setEmailProgress(Math.min(progress, 100));
        if (progress >= 100) {
          clearInterval(finalInterval);
          setTimeout(() => {
            setIsGeneratingEmails(false);
            setGeneratedEmailsProspects(campaign.prospects);
            setShowProspectsList(false);
            setIsEmpty(false);
            setShowGeneratedEmails(true);
            setEmailProgress(0);
          }, 1000);
        }
      }, 30);
    } catch (error) {
      [initialInterval, middleInterval, slowInterval].forEach(clearInterval);
      setIsGeneratingEmails(false);
      setShowProspectsList(false);
      setIsEmpty(false);
      setShowGeneratedEmails(true);
      console.error("Failed to generate emails:", error);
    }
  };

  const handleUpdateEmail = (index: number, newContent: string) => {
    setGeneratedEmailsProspects((prev) => {
      const updated = [...prev];
      updated[index] = {
        ...updated[index],
        emailMessages: [{ from: "me", text: newContent }],
      };
      return updated;
    });
  };

  const handleSaveUpdateEmail = () => {
    setShowEmailEditor(null);
  };

  const toggleProspect = (p: Prospect) => {
    setSelectedProspects((prev: Prospect[]) =>
      prev.some((x) => x.linkedinUrl === p.linkedinUrl)
        ? prev.filter((x) => x.linkedinUrl !== p.linkedinUrl)
        : [...prev, p]
    );
  };

  const toggleAllProspects = () => {
    setSelectedProspects((prev: Prospect[]) =>
      prev.length === prospects.length ? [] : prospects
    );
  };

  const reset = () => {
    setIsCreating(false);
    setIsEmpty(false);
    setShowProspectsList(false);
    setShowGeneratedEmails(false);
    setSelectedProspects([]);
    setProspects([]);
    setShowMessagesView(false);
    setIsGeneratingEmails(false);
    setShowCampaign(false);
    setProgressStep(0);
    setProgressValue(0);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 flex">
        <CampaignSidebar
          campaigns={campaigns}
          onNewCampaign={() => {
            reset();
            setIsCreating(true);
          }}
          onSelectCampaign={(campaign: Campaign, index: number) => {
            reset();
            setShowCampaign(true);
            setSelectedCampaign(campaign);
            setSelectedProspectId(0);
            setSelectedCampaignId(index);
          }}
          selectedCampaignId={selectedCampaignId}
        />

        <main
          className={
            showCampaign
              ? "flex-1"
              : "flex-1 max-w-5xl mx-auto w-full px-4 py-8"
          }
        >
          <div>
            {isLoading && <ProspectProgress progress={progressValue} />}
            {isGeneratingEmails && <EmailProgress progress={emailProgress} />}
            {isCreating && !isLoading && !isGeneratingEmails && (
              <AudienceSearch
                description={description}
                onDescriptionChange={setDescription}
                onExampleClick={handleExampleClick}
                onNext={searchProspects}
              />
            )}
            {showProspectsList && !isLoading && !isGeneratingEmails && (
              <div className="space-y-6">
                <ProspectList
                  prospects={prospects}
                  selectedProspects={selectedProspects}
                  onToggleProspect={toggleProspect}
                  onToggleAll={toggleAllProspects}
                />

                <EmailTemplate
                  emailTemplate={emailTemplate}
                  onEmailTemplateChange={setEmailTemplate}
                  emailStyle={emailStyle}
                  onEmailStyleChange={setEmailStyle}
                  emailLength={emailLength}
                  onEmailLengthChange={setEmailLength}
                  emailTone={emailTone}
                  onEmailToneChange={setEmailTone}
                  selectedCount={selectedProspects.length}
                  onGenerateEmails={handleGenerateEmails}
                />
              </div>
            )}
            {showCampaign && (
              <div className="space-y-6">
                <div className="flex">
                  <div className="h-full max-h-[calc(100vh-4rem)] overflow-y-auto overflow-x-auto flex flex-col justify-stretch">
                    <ProspectStackList
                      prospects={selectedCampaign?.prospects || []}
                      selectedProspectId={selectedProspectId}
                      onSelect={setSelectedProspectId}
                    />
                  </div>
                  <div className="flex-1 h-full">
                    <MessagesPanel
                      messages={(() => {
                        const prospect =
                          selectedCampaign?.prospects[selectedProspectId || 0];
                        if (!prospect || !prospect.emailMessages) return [];
                        return prospect.emailMessages.map(
                          (msg: Email, idx: number) => ({
                            id: `msg-${idx}`,
                            sender: msg.from === "me" ? "me" : "prospect",
                            text: msg.text,
                            timestamp: new Date().toISOString(), // Placeholder, replace with real timestamp if available
                          })
                        );
                      })()}
                      prospectName={getProspectName(
                        selectedCampaign?.prospects[selectedProspectId || 0]
                          ?.firstName +
                          " " +
                          selectedCampaign?.prospects[selectedProspectId || 0]
                            ?.lastName
                      )}
                      name={
                        selectedCampaign?.prospects[selectedProspectId || 0]
                          ?.firstName +
                        " " +
                        selectedCampaign?.prospects[selectedProspectId || 0]
                          ?.lastName
                      }
                    />
                  </div>
                </div>
              </div>
            )}
            {showGeneratedEmails && !isGeneratingEmails && (
              <div>
                <GeneratedEmails
                  prospects={generatedEmailsProspects}
                  showEmailEditor={showEmailEditor}
                  onShowEditor={setShowEmailEditor}
                  onUpdateEmail={handleUpdateEmail}
                  onSaveUpdateEmail={handleSaveUpdateEmail}
                  sendEmails={handleSendEmails}
                />
              </div>
            )}
            {isEmpty && (
              <EmptyState
                onCreateNew={() => {
                  setIsCreating(true);
                  setIsEmpty(false);
                }}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
